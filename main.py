import asyncio
import logging
import os
import random

import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import PREFIX

logging.basicConfig(
    level=logging.INFO,  # Muestra mensajes INFO y superiores
    format="%(asctime)s - %(levelname)s - %(message)s",
)

load_dotenv()

TOKEN: str = os.getenv("TOKEN")


intents: discord.Intents = discord.Intents.default()  # Are like the permissions.
intents.message_content = True  # We can see the message_content.

bot: commands.Bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready() -> None:
    logging.info(f"Bot conectado como {bot.user}")


@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(
        f"🏓 Pong! ({latency} ms)"
    )  # ctx.send sends a message to the channel where the command was written.


@bot.command()
async def trivia(ctx):
    url: str = "https://opentdb.com/api.php?amount=1&type=multiple"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    question_data = data["results"][0]
    question = discord.utils.escape_markdown(question_data["question"])
    correct = discord.utils.escape_markdown(question_data["correct_answer"])
    incorrect = question_data["incorrect_answers"]

    options = incorrect + [correct]
    random.shuffle(options)

    embed: discord.Embed = discord.Embed(
        title="Trivia", description=f"{question}", color=discord.Color.blue()
    )  # Create a embed that will be send later

    for i, option in enumerate(options, start=1):
        embed.add_field(name=f"Opción {i}", value=option, inline=False)

    await ctx.send(embed=embed)  # Whit this we send the embed

    def check(message: discord.Message) -> bool:
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=15.0)
    except asyncio.TimeoutError:
        return await ctx.send(f"Tiempo agotado, la respuesta era **{correct}**")

    if msg.content.strip().lower() == correct.lower():
        await ctx.send(f"Correcto {ctx.author.mention}!")
    else:
        await ctx.send(f"Incorrecto. La respuesta correcta era: **{correct}**")


bot.run(TOKEN)
