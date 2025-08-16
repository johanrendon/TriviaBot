"""Punto de entrada principal para el bot de Discord.

Este script inicializa el bot, configura el registro de logs, carga las
variables de entorno, configura los intents de Discord, carga todas las
extensiones de comandos (cogs) y ejecuta el bot.
"""

import asyncio
import logging
import os
from typing import Final

import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import PREFIX

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

load_dotenv()
TOKEN: Final[str] = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


async def load_cogs() -> None:
    """Busca y carga dinámicamente todos los cogs desde el directorio '/cogs'.

    Esta función itera a través de todos los archivos en el directorio './cogs'.
    Si un archivo termina con '.py', intenta cargarlo como una extensión del bot.
    Registra en logs el resultado (éxito o error) de cada cog.
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logging.info(f"✅ Cog cargado: {filename}")
            except Exception as e:
                logging.error(f"❌ Error al cargar {filename}: {e}")


@bot.event
async def on_ready() -> None:
    """Manejador de evento que se ejecuta cuando el bot se conecta exitosamente a Discord.

    Registra un mensaje de confirmación en la consola y establece la presencia
    del bot como "Jugando Trivia!".
    """
    logging.info(f"🤖 Bot conectado como {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Trivia!"))


async def main() -> None:
    """Función asincrónica principal para ejecutar el bot.

    Esta función sirve como punto de entrada principal. Carga todos los cogs
    y luego inicia el bot, conectándolo a Discord usando el token de las
    variables de entorno.
    """
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
