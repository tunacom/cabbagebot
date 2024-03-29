"""Cabbagebot is a Discord bot that spreads the joy of cabbage."""

import os
import discord
from discord.ext import commands

from cabbage import polyhedral
from cabbage import joy

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!',
                   description='cabbage cabbage cabbages',
                   intents=intents)


@bot.event
async def on_ready():
    """Ready handler."""
    # Let the helpless humans know that the cabbages are active.
    print('CABBAGE TENDRILS EXTENDED INTO INTERTUBES')
    print('CABBAGE CLIENT NAME: {name}'.format(name=bot.user.name))


@bot.command(description='Spread the joy of cabbage!')
async def cabbage(ctx):
    """Spread the joy of cabbage."""
    await ctx.send(joy.spread_joy())


@bot.command(description='キャベツ')
async def キャベツ(ctx):
    """Spread the joy of キャベツ."""
    await ctx.send(joy.spread_joy() + ' desu')


@bot.command(description='SPREAD THE JOY OF CABBAGE!')
async def CABBAGE(ctx):
    """SPREAD THE JOY OF CABBAGE."""
    JOY = joy.create_cabbage_text().upper()
    await ctx.send(JOY)


@bot.command(description='Run level 3 cabbage diagnostic.')
async def diag(ctx):
    """Run a level 3 cabbage diagnostic."""
    info = getattr(joy.get_cabbage, 'diagnostic_info', 'Not available.')[:1400]
    cache_size = len(getattr(joy.get_cabbage, 'cabbage_cache', []))
    diagnostic_message = ('BEEP BOOP. BORING LEVEL 3 DIAGNOSTIC RESULTS:\n\n'
                          'Current cabbage cache size: %d\n'
                          'Previous cabbage response: %s') % (cache_size, info)

    await ctx.send(diagnostic_message)


@bot.command(description='Roll polyhedral cabbages.')
async def roll(ctx, formula: str):
    """Roll polyhedral cabbages based on a formula.

  For example, consider that you are wielding a cabbagebrand longsword in two 
  hands with a +4 strength modifier. You'd need to roll a c10 and c6, and add
  +4 to the result.

  This would look like "!roll c10+c6+4"

  Or let's say you want to cast a spell like cabbageball where you need to roll
  many of the same types of cabbage.

  This would look like "!roll 8c6"

  Args:
    formula: The formula for the roll.
  """
    response = polyhedral.roll_polyhedral_cabbage(formula)
    await ctx.send(response)


def main():
    """Command line cabbages pass through here."""
    flickr_key_path = os.path.join(os.path.dirname(__file__), 'flickr_api_key')
    flickr_key = open(flickr_key_path).read().strip()
    joy.bootstrap(flickr_key)

    # Prepopulate the cabbage cache.
    joy.load_cabbages()

    discord_token_path = os.path.join(os.path.dirname(__file__),
                                      'discord_token')
    discord_token = open(discord_token_path).read().strip()
    bot.run(discord_token)


if __name__ == '__main__':
    main()
