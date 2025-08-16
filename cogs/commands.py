"""A Discord cog for fun and interactive commands.

This cog includes a full trivia game system fetched from the OpenTDB API,
complete with interactive buttons, difficulty selection, and a session-based
leaderboard. It also includes a simple 'ping' command to check bot latency.
"""

import random
from typing import Optional

import aiohttp
import discord
from discord.ext import commands
from discord.ui import Button, View, button


class TriviaView(View):
    """A Discord UI View that presents the trivia options as interactive buttons.

    This view manages the state of the trivia question's buttons, processes user
    interactions, and determines the outcome of the answer.

    Attributes:
        correct_answer (str): The correct answer string for the question.
        author (discord.Member): The user who initiated the trivia command.
        winner (Optional[discord.Member]): The user who answered correctly.
            Defaults to None.
    """

    def __init__(self, correct_answer: str, author: discord.Member):
        """Initializes the TriviaView.

        Args:
            correct_answer: The string of the correct answer.
            author: The member who started the command, who is the only one
                allowed to answer.
        """
        super().__init__(timeout=20.0)
        self.correct_answer = correct_answer
        self.author = author
        self.winner: Optional[discord.Member] = None

    @button(label="Option 1", style=discord.ButtonStyle.primary, emoji="1️⃣")
    async def option_1(self, interaction: discord.Interaction, button: Button) -> None:
        await self.check_answer(interaction, button)

    @button(label="Option 2", style=discord.ButtonStyle.primary, emoji="2️⃣")
    async def option_2(self, interaction: discord.Interaction, button: Button) -> None:
        await self.check_answer(interaction, button)

    @button(label="Option 3", style=discord.ButtonStyle.primary, emoji="3️⃣")
    async def option_3(self, interaction: discord.Interaction, button: Button) -> None:
        await self.check_answer(interaction, button)

    @button(label="Option 4", style=discord.ButtonStyle.primary, emoji="4️⃣")
    async def option_4(self, interaction: discord.Interaction, button: Button) -> None:
        await self.check_answer(interaction, button)

    async def check_answer(
        self, interaction: discord.Interaction, clicked_button: Button
    ) -> None:
        """Callback coroutine for button presses to check the answer.

        This method validates that the interacting user is the one who started
        the trivia. It disables all buttons after the first click, highlights
        the user's choice (green for correct, red for incorrect), shows the
        correct answer if the user was wrong, and stops the view.

        Args:
            interaction: The interaction triggered by the button press.
            clicked_button: The button that was pressed by the user.
        """
        if interaction.user != self.author:
            await interaction.response.send_message(
                "This isn't your trivia! Start your own with the command.",
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
                content=f"Correct, {self.author.mention}! ✅", view=self
            )
        else:
            clicked_button.style = discord.ButtonStyle.danger
            for btn in self.children:
                if isinstance(btn, Button) and btn.label == self.correct_answer:
                    btn.style = discord.ButtonStyle.success
            await interaction.response.edit_message(
                content=f"Incorrect. The answer was **{self.correct_answer}** ❌",
                view=self,
            )

        self.stop()


class FunCommands(commands.Cog):
    """A cog that groups fun-related commands for the bot.

    Attributes:
        bot (commands.Bot): The instance of the Discord bot.
        scores (dict[int, int]): An in-memory dictionary to store user scores,
            mapping user ID to their score.
    """

    def __init__(self, bot: commands.Bot):
        """Initializes the FunCommands cog."""
        self.bot = bot
        self.scores: dict[int, int] = {}

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        """Displays the bot's latency.

        Args:
            ctx: The command invocation context.
        """
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! ({latency} ms)")

    @commands.command()
    async def trivia(self, ctx: commands.Context, difficulty: str = "medium") -> None:
        """Starts a trivia question with multiple-choice answers.

        Fetches a question from the OpenTDB API. The user can specify a
        difficulty. The question is presented in an embed with four buttons
        as answer options. Only the command author can answer.

        Args:
            ctx: The command invocation context.
            difficulty: The desired difficulty ('easy', 'medium', 'hard').
                Defaults to 'medium'.
        """
        valid_difficulties = ["easy", "medium", "hard"]
        if difficulty.lower() not in valid_difficulties:
            await ctx.send("Invalid difficulty. Use `easy`, `medium`, or `hard`.")
            return

        url = f"https://opentdb.com/api.php?amount=1&type=multiple&difficulty={difficulty.lower()}"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        await ctx.send(
                            "Could not contact the trivia API. Please try again later."
                        )
                        return
                    data = await resp.json()
            except aiohttp.ClientError:
                await ctx.send("A connection error occurred with the API.")
                return

        if not data["results"]:
            await ctx.send("Couldn't find any questions for that difficulty.")
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
            title=f"Trivia! ({difficulty.capitalize()})",
            description=f"**{question}**",
            color=discord.Color.purple(),
        )
        embed.set_footer(text=f"Question for {ctx.author.display_name}")

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
                f"{view.winner.mention} now has **{self.scores[user_id]}** points!"
            )

    @commands.command()
    async def leaderboard(self, ctx: commands.Context) -> None:
        """Displays the trivia leaderboard.

        Args:
            ctx: The command invocation context.
        """
        if not self.scores:
            await ctx.send("Nobody has played yet! Be the first with `!trivia`.")
            return

        sorted_scores = sorted(
            self.scores.items(), key=lambda item: item[1], reverse=True
        )

        embed = discord.Embed(
            title="🏆 Trivia Leaderboard 🏆", color=discord.Color.gold()
        )
        description = ""
        for i, (user_id, score) in enumerate(sorted_scores[:10]):
            user = self.bot.get_user(user_id)
            if user:
                description += f"{i + 1}. {user.mention} - **{score}** points\n"

        embed.description = description
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """The setup function required for the bot to load the cog.

    Args:
        bot: The bot instance to which the cog will be added.
    """
    await bot.add_cog(FunCommands(bot))
