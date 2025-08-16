"""Un cog de Discord para comandos divertidos e interactivos.

Este cog incluye un sistema completo de juego de trivia usando la API OpenTDB,
con botones interactivos, selección de dificultad y una tabla de puntuaciones
basada en sesiones. También incluye un comando simple 'ping' para comprobar
la latencia del bot.
"""

import random
from typing import Optional

import aiohttp
import discord
from discord.ext import commands
from discord.ui import Button, View, button


class TriviaView(View):
    """Una vista de Discord que presenta las opciones de trivia como botones interactivos.

    Esta vista maneja el estado de los botones de la pregunta de trivia, procesa
    las interacciones de los usuarios y determina el resultado de la respuesta.

    Atributos:
        correct_answer (str): La respuesta correcta de la pregunta.
        author (discord.Member): El usuario que inició el comando de trivia.
        winner (Optional[discord.Member]): El usuario que respondió correctamente.
            Por defecto es None.
    """

    def __init__(self, correct_answer: str, author: discord.Member):
        """Inicializa la TriviaView.

        Args:
            correct_answer: La cadena con la respuesta correcta.
            author: El miembro que inició el comando, y que es el único autorizado
                a responder.
        """
        super().__init__(timeout=20.0)
        self.correct_answer = correct_answer
        self.author = author
        self.winner: Optional[discord.Member] = None

    @button(label="Opción 1", style=discord.ButtonStyle.primary, emoji="1️⃣")
    async def option_1(self, interaction: discord.Interaction, button: Button) -> None:
        await self.check_answer(interaction, button)

    @button(label="Opción 2", style=discord.ButtonStyle.primary, emoji="2️⃣")
    async def option_2(self, interaction: discord.Interaction, button: Button) -> None:
        await self.check_answer(interaction, button)

    @button(label="Opción 3", style=discord.ButtonStyle.primary, emoji="3️⃣")
    async def option_3(self, interaction: discord.Interaction, button: Button) -> None:
        await self.check_answer(interaction, button)

    @button(label="Opción 4", style=discord.ButtonStyle.primary, emoji="4️⃣")
    async def option_4(self, interaction: discord.Interaction, button: Button) -> None:
        await self.check_answer(interaction, button)

    async def check_answer(
        self, interaction: discord.Interaction, clicked_button: Button
    ) -> None:
        """Corrutina callback para comprobar la respuesta cuando se presiona un botón.

        Este método valida que el usuario que interactúa sea el que inició
        la trivia. Deshabilita todos los botones tras el primer clic, marca la
        elección del usuario (verde si es correcta, rojo si es incorrecta),
        muestra la respuesta correcta si falló y detiene la vista.

        Args:
            interaction: La interacción generada por el clic en el botón.
            clicked_button: El botón presionado por el usuario.
        """
        if interaction.user != self.author:
            await interaction.response.send_message(
                "¡Esta trivia no es tuya! Inicia la tuya con el comando.",
                ephemeral=True,
            )
            return

        for btn in self.children:
            if isinstance(btn, Button):
                btn.disabled = True

        if clicked_button.label == self.correct_answer:
            clicked_button.style = discord.ButtonStyle.success
            self.winner = self.author
            await interaction.response.edit_message(
                content=f"¡Correcto, {self.author.mention}! ✅", view=self
            )
        else:
            clicked_button.style = discord.ButtonStyle.danger
            for btn in self.children:
                if isinstance(btn, Button) and btn.label == self.correct_answer:
                    btn.style = discord.ButtonStyle.success
            await interaction.response.edit_message(
                content=f"Incorrecto. La respuesta era **{self.correct_answer}** ❌",
                view=self,
            )

        self.stop()


class ComandosDivertidos(commands.Cog):
    """Un cog que agrupa los comandos divertidos del bot.

    Atributos:
        bot (commands.Bot): La instancia del bot de Discord.
        scores (dict[int, int]): Un diccionario en memoria para almacenar las
            puntuaciones de los usuarios, mapeando ID de usuario a puntaje.
    """

    def __init__(self, bot: commands.Bot):
        """Inicializa el cog ComandosDivertidos."""
        self.bot = bot
        self.scores: dict[int, int] = {}

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        """Muestra la latencia del bot.

        Args:
            ctx: El contexto de invocación del comando.
        """
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 ¡Pong! ({latency} ms)")

    @commands.command()
    async def trivia(self, ctx: commands.Context, difficulty: str = "medium") -> None:
        """Inicia una pregunta de trivia con opciones múltiples.

        Obtiene una pregunta desde la API OpenTDB. El usuario puede especificar
        la dificultad. La pregunta se muestra en un embed con cuatro botones
        como opciones de respuesta. Solo el autor del comando puede responder.

        Args:
            ctx: El contexto de invocación del comando.
            difficulty: La dificultad deseada ('easy', 'medium', 'hard').
                Por defecto es 'medium'.
        """
        valid_difficulties = ["easy", "medium", "hard"]
        if difficulty.lower() not in valid_difficulties:
            await ctx.send("Dificultad inválida. Usa `easy`, `medium` o `hard`.")
            return

        url = f"https://opentdb.com/api.php?amount=1&type=multiple&difficulty={difficulty.lower()}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        await ctx.send(
                            "No se pudo contactar con la API de trivia. Intenta más tarde."
                        )
                        return
                    data = await resp.json()
            except aiohttp.ClientError:
                await ctx.send("Ocurrió un error de conexión con la API.")
                return

        if not data["results"]:
            await ctx.send("No se encontraron preguntas para esa dificultad.")
            return

        question_data = data["results"][0]
        question = discord.utils.escape_markdown(question_data["question"])
        correct = discord.utils.escape_markdown(question_data["correct_answer"])
        incorrect = [
            discord.utils.escape_markdown(ans)
            for ans in question_data["incorrect_answers"]
        ]

        options = incorrect + [correct]
        random.shuffle(options)

        embed = discord.Embed(
            title=f"Trivia ({difficulty.capitalize()})",
            description=f"**{question}**",
            color=discord.Color.purple(),
        )
        embed.set_footer(text=f"Pregunta para {ctx.author.display_name}")

        view = TriviaView(correct_answer=correct, author=ctx.author)
        for i, option in enumerate(options):
            if i < len(view.children) and isinstance(view.children[i], Button):
                view.children[i].label = option

        await ctx.send(embed=embed, view=view)
        await view.wait()

        if view.winner:
            user_id = view.winner.id
            self.scores[user_id] = self.scores.get(user_id, 0) + 1
            await ctx.send(
                f"{view.winner.mention} ahora tiene **{self.scores[user_id]}** puntos!"
            )

    @commands.command()
    async def leaderboard(self, ctx: commands.Context) -> None:
        """Muestra la tabla de posiciones de la trivia.

        Args:
            ctx: El contexto de invocación del comando.
        """
        if not self.scores:
            await ctx.send("¡Nadie ha jugado todavía! Sé el primero con `!trivia`.")
            return

        sorted_scores = sorted(
            self.scores.items(), key=lambda item: item[1], reverse=True
        )

        embed = discord.Embed(
            title="🏆 Tabla de posiciones de Trivia 🏆", color=discord.Color.gold()
        )
        description = ""
        for i, (user_id, score) in enumerate(sorted_scores[:10]):
            user = self.bot.get_user(user_id)
            if user:
                description += f"{i + 1}. {user.mention} - **{score}** puntos\n"

        embed.description = description
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Función de configuración requerida para que el bot cargue el cog.

    Args:
        bot: La instancia del bot al que se añadirá el cog.
    """
    await bot.add_cog(ComandosDivertidos(bot))
