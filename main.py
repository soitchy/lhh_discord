import discord
import sys
import sqlite3
import re

from discord.ext import commands

# TODOS:
# - add a disconnect function to cleanly close the db and whatever
# - add a way for the bot to decrement a member's count if their message is deleted by an admin

# Table "member_stats":
#    id: INT PRIMARY KEY -> id refers to the discord unique id
#    total_messages: INT NOT NULL
#    plug_credits: INT NOT NULL
#    feedback_credits: INT NOT NULL



# Globals
MEMBER_STATS_TABLE = 'member_stats'
COL_MESSAGE_COUNT = 'total_messages'
COL_PLUG_CREDITS = 'plug_credits'
COL_FEEDBACK_CREDITS = 'feedback_credits'

client = discord.Client()
con = sqlite3.connect('db/lhh.db')
bot = commands.Bot(command_prefix='!')

con.row_factory = sqlite3.Row

@bot.event
async def on_ready():
    print(f'{bot.user} has connected.')

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    urls = find_urls(message.content)
    print(f'{message.type}, {message.channel}, {message.author}, -> {message.content}')
    print(f'Reference: {message.reference}')
    print(f'Embeds: {message.embeds}')
    print(f'Attachments: {message.attachments}')
    print(f'Flags: {message.flags}')
    print(f'URLs: {urls}')
    print(f'Author Roles: {message.author.roles}')
    print('')

    # Add the member to the DB if they dont exist
    member_tup = fetch_member(message.author.id)
    if member_tup == None:
        print(f'{message.author.id} was not found in the database. Adding.')
        insert_member(message.author.id)
        member_tup = (message.author.id, 1, 0, 0) # overwriting the row variable, as it would be None otherwise
    
    # Update stats
    incrememt_message_count(message.author.id)
    if len(message.content) > 10:
        # print('Message longer than 10 characters. Adding plug credit.')
        add_plug_credit(message.author.id)
    
    # Handle links
    if len(urls) > 0 and message.channel.name != 'feedback':
        if message.channel.name == 'shameless-self-plug' and member_tup[2] < 20:
            await message.channel.send(f'You have already met your plug quota to post links in this channel, {message.author.mention}. Please chat a bit more before reposting in this channel.')
            await message.delete()
            return
        elif message.channel.name == 'shameless-self-plug' and member_tup[2] >= 20:
            reset_plug_credits(message.author.id)
            return
        elif not any(role.name in ('Regulars', 'badmin') for role in message.author.roles) and member_tup[1] < 20:
            await message.channel.send(f'You do not yet have permission to send links in this channel, {message.author.mention}. You must chat a bit more before you are allowed to send links.')
            await message.delete()
            return

    await bot.process_commands(message)

@bot.command(name='stats')
async def stats(ctx):
    row_tup = fetch_member(ctx.author.id)
    if row_tup == None:
        await ctx.send('You have not sent any messages in this server yet.')
    else:
        plug_access = row_tup[2] > 20
        await ctx.send(f'You have sent {row_tup[1]} messages since I started counting. Plug access: {plug_access}')

@bot.command(name='ping')
async def test(ctx):
    await ctx.send(f'{ctx.message.author.mention}')


def fetch_member(id):
    cur = con.cursor()

    cur.execute(f'select * from {MEMBER_STATS_TABLE} where id = {id}')
    row = cur.fetchone()
    cur.close()
    
    row_tup = tuple(row) if row != None else None

    return row_tup

def insert_member(id):
    db_execute(f'insert into {MEMBER_STATS_TABLE} values ({id}, 1, 0, 0)')

def incrememt_message_count(id):
    db_execute(f'update {MEMBER_STATS_TABLE} set {COL_MESSAGE_COUNT} = {COL_MESSAGE_COUNT} + 1 where id = {id}')

def add_plug_credit(id):
    db_execute(f'update {MEMBER_STATS_TABLE} set {COL_PLUG_CREDITS} = {COL_PLUG_CREDITS} + 1 where id = {id}')

def reset_plug_credits(id):
    db_execute(f'update {MEMBER_STATS_TABLE} set {COL_PLUG_CREDITS} = 0 where id = {id}')

def db_execute(command):
    cur = con.cursor()
    cur.execute(command)
    con.commit()
    cur.close()

def find_urls(content):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, content)      
    return [x[0] for x in url]


bot.run(sys.argv[1])
