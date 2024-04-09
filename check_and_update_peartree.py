import discord
from discord.ext import commands
import shutil
import json
import os

def same_jsons(file1_path, file2_path):
    """Check if 2 json files are the same."""
    # Read the content of the first JSON file
    with open(file1_path, 'r') as file1:
        content1 = file1.read()

    # Read the content of the second JSON file
    with open(file2_path, 'r') as file2:
        content2 = file2.read()

    # Parse the JSON content into Python objects
    data1 = json.loads(content1)
    data2 = json.loads(content2)

    # Compare the Python objects for equality
    return data1 == data2
        

def copy_json(source_path, destination_path):
    """Copy source file to destination file."""
    shutil.copyfile(source_path, destination_path)
    print(f'File copied from {source_path} to {destination_path}')


def send_to_discord(file_path):
    """Use Discord bot to send results to channel."""
    
    with open(file_path, 'r') as file:
        content = file.read()
    res = json.loads(content)

    # GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
    bot = discord.Client()

    # Event triggered when the bot is ready
    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name} ({bot.user.id})')
        channel = bot.get_channel(1213971777655668836) 
        embed = discord.Embed(
            title='🍐🌲 Peartree apartment price update',
            description='[Check latest prices](https://www.peartreeapts.com/#sightmap-1)',
            color=discord.Color.blue()
        )
        
        # Add fields to the embed
        for _res in res: 
            value_str = f"**Unit price:** ${_res['price']:,}\n**Available:** {_res['available_on']} ({_res['display_lease_term']}-month lease)"
            embed.add_field(name=f"🏠 Unit #{_res['unit_number']}", value=value_str, inline=False)
        
        await channel.send(embed=embed)
        await bot.close()

    # EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    assert DISCORD_TOKEN is not None, "No DISCORD_TOKEN. You need to set token as environment variable!"
    bot.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
    snapshot_path = 'old_prices_peartree.json'
    latest_path = 'newest_prices_peartree.json'

    if not same_jsons(latest_path, snapshot_path):
        # Send latest result to Discord
        print("Price update! Send latest info to Discord.")
        send_to_discord(latest_path)

        # Replace snapshot json
        print("Replace snapshot with latest file.")
        copy_json(latest_path, snapshot_path)
    else: 
        print('No price change.')
        