"""/task commands: a shared to-do list per server (great for group projects)."""
import discord
from discord import app_commands
from discord.ext import commands

import db


class Tasks(commands.GroupCog, group_name="task"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="add", description="Add a task to this server's to-do list")
    @app_commands.describe(text="What needs to be done")
    async def add(self, interaction: discord.Interaction, text: str):
        if interaction.guild_id is None:
            return await interaction.response.send_message("Use this in a server.", ephemeral=True)
        task_id = await db.add_task(interaction.guild_id, interaction.user.id, text[:200])
        await interaction.response.send_message(f"Added task **#{task_id}**: {text[:200]}")

    @app_commands.command(name="list", description="Show open tasks")
    async def list_(self, interaction: discord.Interaction):
        if interaction.guild_id is None:
            return await interaction.response.send_message("Use this in a server.", ephemeral=True)
        rows = await db.list_tasks(interaction.guild_id)
        if not rows:
            return await interaction.response.send_message("No open tasks. Nice work!")
        lines = [f"**#{tid}** {text} — <@{author}>" for tid, author, text, _ in rows]
        embed = discord.Embed(title="Open tasks", description="\n".join(lines), color=0x5865F2)
        await interaction.response.send_message(
            embed=embed, allowed_mentions=discord.AllowedMentions.none()
        )

    @app_commands.command(name="done", description="Mark a task as done")
    @app_commands.describe(task_id="The task number shown in /task list")
    async def done(self, interaction: discord.Interaction, task_id: int):
        if interaction.guild_id is None:
            return await interaction.response.send_message("Use this in a server.", ephemeral=True)
        if await db.complete_task(interaction.guild_id, task_id):
            await interaction.response.send_message(f"Task **#{task_id}** done ✅")
        else:
            await interaction.response.send_message(f"No open task #{task_id}.", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Tasks(bot))
