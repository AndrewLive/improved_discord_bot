import os, discord
from typing import Any, List, Mapping, Optional
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import Command, Group
from dotenv import load_dotenv
from discord.ext import commands, tasks

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping: Mapping):
        for cog in mapping:
            if cog == None:
                continue
            await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in mapping[cog]]}')
        
        return

    async def send_cog_help(self, cog: Cog) -> None:
        await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in cog.get_commands()]}')
    
    async def send_group_help(self, group: Group):
        return await super().send_group_help(group)
    
    async def send_command_help(self, command: Command):
        await self.get_destination().send(command.name)