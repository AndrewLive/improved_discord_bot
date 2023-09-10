import os, discord
from typing import Any, List, Mapping, Optional
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import Command, Group
from dotenv import load_dotenv
from discord.ext import commands, tasks

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping: Mapping[Cog | None, List[Command[Any, Callable[..., Any], Any]]]) -> None:
        return await super().send_bot_help(mapping)

    async def send_cog_help(self, cog: Cog) -> None:
        return await super().send_cog_help(cog)
    
    async def send_group_help(self, group: Group[Any, Callable[..., Any], Any]) -> None:
        return await super().send_group_help(group)
    
    async def send_command_help(self, command: Command[Any, Callable[..., Any], Any]) -> None:
        return await super().send_command_help(command)