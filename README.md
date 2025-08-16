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
    ```

2. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

### 🔑 Token Configuration

This bot uses environment variables for better security.
You must create a `.env` file in the root of the project with the following content:

    TOKEN=YOUR_DISCORD_BOT_TOKEN_HERE

👉 Replace `YOUR_DISCORD_BOT_TOKEN_HERE` with your bot’s token generated in the [Discord Developer Portal](https://discord.com/developers/applications).

### 🔧 Configuration in the Discord Developer Portal

Before running the bot, you need to configure some settings in the Discord Developer Portal to ensure it has the necessary permissions to function.

#### Enabling Privileged Intents

For the bot to read messages (like answers to trivia) and recognize server members, you must enable two "Privileged Intents".

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and select your application.
2. In the left-hand menu, click on the **"Bot"** tab.
3. Scroll down to the **"Privileged Gateway Intents"** section.
4. Enable the following options:
    - **SERVER MEMBERS INTENT**: Allows the bot to receive events related to server members (e.g., when someone joins).
    - **MESSAGE CONTENT INTENT**: Allows the bot to read the content of messages. This is crucial for commands and trivia answers.
5. Don't forget to save your changes!

#### 🔗 Inviting the Bot to Your Server

Once configured, you can generate an invitation link to add the bot to any server where you have administrative permissions.

1. Within your application in the portal, go to the **"OAuth2"** tab and then to **"URL Generator"**.
2. In the **"SCOPES"** section, check the `bot` and `applications.commands` boxes.
3. A new section called **"BOT PERMISSIONS"** will appear. Here, you must select the permissions the bot needs to function correctly:
    - `Send Messages`
    - `Read Message History` (necessary to see previous messages in a channel)
    - `Add Reactions` (used for trivia answer feedback)
4. Copy the URL generated at the bottom and paste it into your browser.
5. Select the server you want to invite the bot to and authorize the permissions.

## ▶️ Running the Bot

To start the bot:

```bash
python main.py
```

If everything is set up correctly, you should see in the console:

🤖 Bot connected as BOT_NAME

## 📦 Main Dependencies

Some of the libraries included in requirements.txt:

    discord.py → For interacting with the Discord API.

    aiohttp → For making HTTP requests to the Trivia API.

## 🎮 Commands

Here are the available commands to interact with the bot.

### 🧠 `!trivia`

Starts a new trivia game. The bot will send a multiple-choice question. If the user who ran the command answers correctly, they will earn one point, which will be recorded on the leaderboard.

### 🏆 `!leaderboard`

Displays the server's current leaderboard. You can see who is winning and how many points each player has. Scores are reset if the bot is turned off.

### 🏓 `!ping`

Checks the bot's latency. This command will respond with the current response time in milliseconds (ms), letting you know if the bot is running quickly and efficiently.python-dotenv → For managing environment variables easily.

## 📝 Notes

    Only the user who runs the !trivia command can answer.

    Scores are stored in memory while the bot is running (not in a database).

    The bot prefix is configured in config.py.

## 📜 License

This project is free to use for educational and personal purposes.
