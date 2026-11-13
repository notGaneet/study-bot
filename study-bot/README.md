# Study Bot 📚

A Discord bot that helps study groups stay organized: shared to-do lists, and soon reminders, polls and flashcard quizzes.

## Features

| Command            | What it does                                 |
| ------------------ | -------------------------------------------- |
| `/ping`            | Check the bot is online                      |
| `/task add <text>` | Add a task to the server's shared to-do list |
| `/task list`       | Show open tasks                              |
| `/task done <id>`  | Mark a task done                             |

**Roadmap:** `/remind`, `/poll`, `/flashcard add`, `/flashcard quiz`

## Tech stack

Python · discord.py (slash commands, cogs) · SQLite (aiosqlite) · pytest · GitHub Actions

## Run it yourself

1. Create a bot at the [Discord Developer Portal](https://discord.com/developers/applications) → **Bot** → copy the token.
2. Invite it: **OAuth2 → URL Generator** -> scopes `bot` + `applications.commands` -> permissions _Send Messages_, _Embed Links_ -> open the URL.
3. Set up and run:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env             # then paste your token (and test server ID)
python bot.py
```

## Tests

```bash
pytest -v
```

## Project structure

```
bot.py          # starts the bot, loads cogs, syncs slash commands
db.py           # all SQLite access
cogs/           # one file per feature
tests/          # pytest tests for the database layer
```
