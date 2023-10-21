# improved_discord_bot

A discord bot for me and my friends.
Functions include:

- Text translation using Google Translate's API
- Status retrieval and discord <-> server communication with a locally hosted Minecraft server
- Retrieval of a random 100% real totally-not-made-up quote from Ancient Chinese General, Sun Tzu
- Blackjack played throught discord embeds

## Package dependencies

The modules in used for this bot depend on the following python packages (versions are the ones currently used):

- discord
- dotenv
- googletrans 3.1.0a0 or later
  - must be the specified version to avoid "'None' type has no member 'Group'" error
- mcstatus
- gtts (google text to speech)
- datetime

The following unix applications are also required:

- FFMPEG


## Command usage

Bot commands are invoked with the prefix `l.<command>`. The following commands are available:

    Minecraft:
        minecraft    Returns information about the Denny's Minecraft Server
        rconsay      Sends a message to the Minecraft server chat
    SunTzu:
        reloadsuntzu Reloads the list of quotes that Sun Tzu can give (only usable by bot owner)
        suntzu       Gives a 100% real quote from ancient Chinese general Sun Tzu
    Translate:
        translate    Translates the message the invoker replied to
    ​No Category:
        help         Shows this message

    Type l.help command for more info on a command.
    You can also type l.help category for more info on a category.
