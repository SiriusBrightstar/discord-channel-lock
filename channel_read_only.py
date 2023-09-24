import os
from datetime import date
from discord import Client
from discord import Intents
from dotenv import dotenv_values
from nsepython import nse_holidays
from pandas import json_normalize as jn

cred = dotenv_values()

# Set up the Discord client
intents = Intents.default()
intents.members = True  # To get member updates
client = Client(intents=intents)


def is_market_closed_today() -> list:
    # Function that returns a list:
    # [bool is_market_closed_today, if true: string reason]
    pd_holidays = jn(nse_holidays('trading')['FO'])
    today = date.today().strftime('%d-%b-%Y')
    is_holiday = today in pd_holidays['tradingDate'].values

    if is_holiday:
        reason_row = pd_holidays.loc[pd_holidays['tradingDate']
                                     == today]
        reason = reason_row['description'].to_list()[0]
        print(f'Holiday Reason: {reason}')
        return [True, reason]
    else:
        print('Not a Holiday')
        return [False]


async def make_channel_read_only():
    # Function to change channel permissions to read-only
    channel = client.get_channel(int(cred['DISCORD_CHANNEL_ID']))

    holiday = is_market_closed_today()
    if holiday[0] == False:
        # read_only_role = channel.guild.get_role(int(cred['READ_ONLY_ROLE_ID']))
        read_only_role_2 = channel.guild.get_role(int(cred['READ_ONLY_ROLE_ID_2']))
        await channel.send(f'This Channel is locked till 15:30🔒.\nGo to <#{int(cred["OPEN_CHANNEL_ID"])}> or any other serious channels.')
        # Set read-only permission for the read-only role
        # await channel.set_permissions(read_only_role, read_messages=True, send_messages=False)
        await channel.set_permissions(read_only_role_2, read_messages=True, send_messages=False)
        print(f"Channel {channel.name} is now read-only for {read_only_role_2.name}.")
    else:
        print('Today is a Holiday')
        await channel.send(f'Markets are Closed today\nHappy {holiday[1]}')


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')
    print('------')
    await make_channel_read_only()

    os._exit(0)

# Run the Discord client
client.run(cred['DISCORD_TOKEN'])
