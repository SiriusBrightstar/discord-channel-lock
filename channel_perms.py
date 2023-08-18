import os
from discord import Client
from discord import Intents
from dotenv import dotenv_values

cred = dotenv_values()

# Set up the Discord client
intents = Intents.default()
intents.members = True  # To get member updates
client = Client(intents=intents)


async def make_channel_read_only():
    # Function to change channel permissions to read-only
    channel = client.get_channel(int(cred['DISCORD_CHANNEL_ID']))
    read_only_role = channel.guild.get_role(int(cred['READ_ONLY_ROLE_ID']))
    await channel.send('This Channel is locked till 15:30IST. Go to <#1053640650094034955>')
    # Set read-only permission for the read-only role
    await channel.set_permissions(read_only_role, read_messages=True, send_messages=False)
    print(f"Channel {channel.name} is now read-only.")


async def make_channel_read_write():
    # Function to change channel permissions to read & write
    channel = client.get_channel(int(cred['DISCORD_CHANNEL_ID']))
    read_only_role = channel.guild.get_role(int(cred['READ_ONLY_ROLE_ID']))

    # Set read-only permission for the read-only role
    await channel.set_permissions(read_only_role, read_messages=True, send_messages=True)
    print(f"Channel {channel.name} is now read & write.")


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    print('------')
    # Select which ever function is required
    await make_channel_read_only()
    # await make_channel_read_write()

    os._exit(0)

# Run the Discord client
client.run(cred['DISCORD_TOKEN'])
