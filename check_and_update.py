import discord
from discord.ext import commands
import shutil
import json
import os

def are_json_files_equal(file1_path, file2_path):
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
        channel = bot.get_channel(1084864988688154627) 
        embed = discord.Embed(
            title='🏡 Rental price update!',
            description='Check https://liveat678bellflower.com/floor-plans.aspx.',
            color=discord.Color.blue()
        )
        
        # Add fields to the embed
        for _res in res: 
            value_str = f"${_res['unit_price']:,}, available {_res['available_date']} for {_res['lease_term']}-month lease"
            embed.add_field(name=f"🏠 Unit #{_res['unit_number']}", value=value_str, inline=False)
        
        await channel.send(embed=embed)
        await bot.close()

    # EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
    bot.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
    snapshot_path = 'snapshot_prices.json'
    latest_path = 'latest_prices.json'

    if not are_json_files_equal(latest_path, snapshot_path):
        # Send latest result to Discord
        print("Send latest info to Discord.")
        send_to_discord(latest_path)

        # Replace snapshot json
        print("Replace snapshot with latest file.")
        copy_json(latest_path, snapshot_path)
        