"""Cabbagebot is a Discord bot that spreads the joy of cabbage."""

import os
from discord.ext import commands

from cabbage import polyhedral
from cabbage import joy

bot = commands.Bot(command_prefix='!', description='cabbage cabbage cabbages')


@bot.event
async def on_ready():
  """Ready handler."""
  # Let the helpless humans know that the cabbages are active.
  print('CABBAGE TENDRILS EXTENDED INTO INTERTUBES')
  print('CABBAGE CLIENT NAME: {name}'.format(name=bot.user.name))


@bot.command(description='Spread the joy of cabbage!')
async def cabbage():
  """Spread the joy of cabbage."""
  await bot.say(joy.spread_joy())


@bot.command(description='SPREAD THE JOY OF CABBAGE!')
async def CABBAGE():
  """SPREAD THE JOY OF CABBAGE."""
  JOY = joy.create_cabbage_text().upper()
  await bot.say(JOY)


@bot.command(description='Roll polyhedral cabbages.')
async def roll(formula : str):
  """Roll a polyhedral cabbage.

  Args:
    formula: The formula for the roll.
  """
  response = polyhedral.roll_polyhedral_cabbage(formula)
  await bot.say(response)


def main():
  """Command line cabbages pass through here."""
  flickr_key_path = os.path.join(os.path.dirname(__file__), 'flickr_api_key')
  flickr_key = open(flickr_key_path).read().strip()
  joy.bootstrap(flickr_key)

  # Prepopulate the cabbage cache.
  joy.load_cabbages()

  discord_token_path = os.path.join(os.path.dirname(__file__), 'discord_token')
  discord_token = open(discord_token_path).read().strip()
  bot.run(discord_token)


if __name__ == '__main__':
  main()
