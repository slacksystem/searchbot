"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.5.0
"""

import discord
import pendulum
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


class Owner(commands.Cog, name="owner"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @staticmethod
    def _matches_search_filters(
        message: discord.Message,
        user: discord.User = None,
        message_query: str = None,
        mentions: discord.User = None,
        before: pendulum.DateTime = None,
        after: pendulum.DateTime = None,
    ) -> bool:
        if user is not None and message.author.id != user.id:
            return False
        if (
            message_query is not None
            and message_query.lower() not in message.clean_content.lower()
        ):
            return False
        if mentions is not None and not any(u.id == mentions.id for u in message.mentions):
            return False
        if before is not None and message.created_at >= before:
            return False
        if after is not None and message.created_at <= after:
            return False
        return True

    @commands.command(
        name="sync",
        description="Synchonizes the slash commands.",
    )
    @app_commands.describe(scope="The scope of the sync. Can be `global` or `guild`")
    @commands.is_owner()
    async def sync(self, context: Context, scope: str) -> None:
        """
        Synchonizes the slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global` or `guild`.
        """

        if scope == "global":
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Slash commands have been globally synchronized.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.copy_global_to(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Slash commands have been synchronized in this guild.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="The scope must be `global` or `guild`.", color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.command(
        name="unsync",
        description="Unsynchonizes the slash commands.",
    )
    @app_commands.describe(
        scope="The scope of the sync. Can be `global`, `current_guild` or `guild`"
    )
    @commands.is_owner()
    async def unsync(self, context: Context, scope: str) -> None:
        """
        Unsynchonizes the slash commands.

        :param context: The command context.
        :param scope: The scope of the sync. Can be `global`, `current_guild` or `guild`.
        """

        if scope == "global":
            context.bot.tree.clear_commands(guild=None)
            await context.bot.tree.sync()
            embed = discord.Embed(
                description="Slash commands have been globally unsynchronized.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        elif scope == "guild":
            context.bot.tree.clear_commands(guild=context.guild)
            await context.bot.tree.sync(guild=context.guild)
            embed = discord.Embed(
                description="Slash commands have been unsynchronized in this guild.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description="The scope must be `global` or `guild`.", color=0xE02B2B
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="load",
        description="Load a cog",
    )
    @app_commands.describe(cog="The name of the cog to load")
    @commands.is_owner()
    async def load(self, context: Context, cog: str) -> None:
        """
        The bot will load the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to load.
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not load the `{cog}` cog.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Successfully loaded the `{cog}` cog.", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="unload",
        description="Unloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to unload")
    @commands.is_owner()
    async def unload(self, context: Context, cog: str) -> None:
        """
        The bot will unload the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to unload.
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not unload the `{cog}` cog.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Successfully unloaded the `{cog}` cog.", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="reload",
        description="Reloads a cog.",
    )
    @app_commands.describe(cog="The name of the cog to reload")
    @commands.is_owner()
    async def reload(self, context: Context, cog: str) -> None:
        """
        The bot will reload the given cog.

        :param context: The hybrid command context.
        :param cog: The name of the cog to reload.
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception:
            embed = discord.Embed(
                description=f"Could not reload the `{cog}` cog.", color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        embed = discord.Embed(
            description=f"Successfully reloaded the `{cog}` cog.", color=0xBEBEFE
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @commands.is_owner()
    async def shutdown(self, context: Context) -> None:
        """
        Shuts down the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(description="Shutting down. Bye! :wave:", color=0xBEBEFE)
        await context.send(embed=embed)
        await self.bot.close()

    @commands.hybrid_command(
        name="say",
        description="The bot will say anything you want.",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @commands.is_owner()
    async def say(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        await context.send(message)

    @commands.hybrid_command(
        name="embed",
        description="The bot will say anything you want, but within embeds.",
    )
    @app_commands.describe(message="The message that should be repeated by the bot")
    @commands.is_owner()
    async def embed(self, context: Context, *, message: str) -> None:
        """
        The bot will say anything you want, but using embeds.

        :param context: The hybrid command context.
        :param message: The message that should be repeated by the bot.
        """
        embed = discord.Embed(description=message, color=0xBEBEFE)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="search",
        description="Search messages across user DMs.",
    )
    @app_commands.describe(
        user="Filter by message author.",
        message="Filter by text contained in the message.",
        mentions="Filter by messages that mention this user.",
        before="Only include messages before this datetime.",
        after="Only include messages after this datetime.",
        limit="How many recent messages to check per DM channel (max 1000).",
    )
    @commands.is_owner()
    async def search(
        self,
        context: Context,
        user: discord.User = None,
        limit: app_commands.Range[int, 1, 1000] = 100,
        *,
        message: str = None,
        mentions: discord.User = None,
        before: str = None,
        after: str = None,
    ) -> None:
        """
        Search messages across all DM channels visible to the bot.

        :param context: The hybrid command context.
        :param user: Filter by message author.
        :param message: Filter by text content.
        :param mentions: Filter by mentioned user.
        :param before: Filter for messages before this datetime.
        :param after: Filter for messages after this datetime.
        :param limit: Number of recent messages to inspect per DM channel.
        """
        if context.interaction is not None:
            await context.interaction.response.defer()

        parsed_before = None
        parsed_after = None
        if before is not None:
            try:
                parsed_before = pendulum.parse(before, strict=False, tz="UTC")
            except Exception:
                embed = discord.Embed(
                    description="Invalid `before` datetime. Use an ISO-like value, e.g. `2026-07-01T12:30:00Z`.",
                    color=0xE02B2B,
                )
                await context.send(embed=embed)
                return
        if after is not None:
            try:
                parsed_after = pendulum.parse(after, strict=False, tz="UTC")
            except Exception:
                embed = discord.Embed(
                    description="Invalid `after` datetime. Use an ISO-like value, e.g. `2026-07-01T12:30:00Z`.",
                    color=0xE02B2B,
                )
                await context.send(embed=embed)
                return

        if user is None and message is None and mentions is None and before is None and after is None:
            embed = discord.Embed(
                description="Please provide at least one filter: `user`, `message`, `mentions`, `before`, or `after`.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return

        matched_messages = []
        for channel in self.bot.private_channels:
            if not isinstance(channel, discord.DMChannel):
                continue
            async for dm_message in channel.history(limit=limit):
                if self._matches_search_filters(
                    dm_message, user, message, mentions, parsed_before, parsed_after
                ):
                    matched_messages.append(dm_message)

        if not matched_messages:
            embed = discord.Embed(
                description="No DM messages matched the provided filters.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
            return

        shown_messages = sorted(
            matched_messages,
            key=lambda dm_message: dm_message.created_at,
            reverse=True,
        )[:10]
        result_lines = []
        for dm_message in shown_messages:
            channel_user = dm_message.channel.recipient
            channel_user_text = (
                f"{channel_user} ({channel_user.id})"
                if channel_user is not None
                else f"Unknown ({dm_message.channel.id})"
            )
            content = dm_message.clean_content if dm_message.clean_content else "[no text]"
            if len(content) > 120:
                content = f"{content[:117]}..."
            result_lines.append(
                f"• [{dm_message.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {dm_message.author} in DM with {channel_user_text}: {content}"
            )

        embed = discord.Embed(
            title="DM Search Results",
            description="\n".join(result_lines),
            color=0xBEBEFE,
        )
        embed.set_footer(
            text=f"Found {len(matched_messages)} match(es), showing {len(shown_messages)}."
        )
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(Owner(bot))
