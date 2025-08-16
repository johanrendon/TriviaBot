# 🤖 Discord Bot - Trivia and Fun Commands

This project is a Discord bot that includes:

- 🎮 A complete **Trivia** system using the OpenTDB API.
- 🏓 A **ping** command to check the bot's latency.
- 🏆 A real-time trivia leaderboard.
- ⚙️ A modular architecture with **cogs** to organize commands.

## 🚀 Installation

1. **Clone the repository**

   ```bash
   git clone <REPOSITORY_URL>
   cd <PROJECT_NAME>

    Install dependencies

    pip install -r requirements.txt

🔑 Token Configuration

This bot uses environment variables for better security.
You must create a .env file in the root of the project with the following content:

    TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE

👉 Replace YOUR_DISCORD_BOT_TOKEN_HERE with your bot’s token generated in the [Discord Developer Portal](https://discord.com/developers/applications).

## ▶️ Running the Bot

To start the bot:

```bash
python main.py
```

If everything is set up correctly, you should see in the console:

    🤖 Bot connected as BOT_NAME

📦 Main Dependencies

Some of the libraries included in requirements.txt:

    discord.py → For interacting with the Discord API.

    aiohttp → For making HTTP requests to the Trivia API.

    python-dotenv → For managing environment variables easily.

📝 Notes

    Only the user who runs the !trivia command can answer.

    Scores are stored in memory while the bot is running (not in a database).

    The bot prefix is configured in config.py.

📜 License

This project is free to use for educational and personal purposes.
