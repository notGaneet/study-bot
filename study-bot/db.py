"""Small async SQLite layer. All database access goes through here."""
import os

import aiosqlite

DB_PATH = os.getenv("DB_PATH", "studybot.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id    INTEGER NOT NULL,
    author_id   INTEGER NOT NULL,
    text        TEXT    NOT NULL,
    done        INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


async def init_db(path: str = None):
    async with aiosqlite.connect(path or DB_PATH) as conn:
        await conn.executescript(SCHEMA)
        await conn.commit()


async def add_task(guild_id: int, author_id: int, text: str, path: str = None) -> int:
    async with aiosqlite.connect(path or DB_PATH) as conn:
        cur = await conn.execute(
            "INSERT INTO tasks (guild_id, author_id, text) VALUES (?, ?, ?)",
            (guild_id, author_id, text),
        )
        await conn.commit()
        return cur.lastrowid


async def list_tasks(guild_id: int, include_done: bool = False, path: str = None):
    query = "SELECT id, author_id, text, done FROM tasks WHERE guild_id = ?"
    if not include_done:
        query += " AND done = 0"
    query += " ORDER BY id"
    async with aiosqlite.connect(path or DB_PATH) as conn:
        cur = await conn.execute(query, (guild_id,))
        return await cur.fetchall()


async def complete_task(guild_id: int, task_id: int, path: str = None) -> bool:
    """Mark a task done. Returns False if no open task with that id exists in this server."""
    async with aiosqlite.connect(path or DB_PATH) as conn:
        cur = await conn.execute(
            "UPDATE tasks SET done = 1 WHERE id = ? AND guild_id = ? AND done = 0",
            (task_id, guild_id),
        )
        await conn.commit()
        return cur.rowcount > 0
