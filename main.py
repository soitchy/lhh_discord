import discord
import sys
import sqlite3
import re

from discord.ext import commands

# TODOS:
# - add a disconnect function to cleanly close the db and whatever
# - add a way for the bot to decrement a member's count if their message is deleted by an admin
# - add a column tracking the "running count" required for plugs
# - add a way reset the running count when a member shares a link
#     > how do we handle non links ie just general chit chat in the channel?
# - only count messages that are in specific channels
#   > blacklist: fishing, memes, server-history, misc-bot, misc-voice, time-out
#   > or rather, add a command to set the specific feedback and plug channels
#   > and perhaps onyl count messages over a certain char length. 10?

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
    if message.author == bot.user:
        return

    urls = find_urls(message.content)
    print(f'{message.type}, {message.channel}, {message.author}, -> {message.content}')
    print(f'Reference: {message.reference}')
    print(f'Embeds: {message.embeds}')
    print(f'Attachments: {message.attachments}')
    print(f'Flags: {message.flags}')
    print(f'URLs: {urls}')

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

    # Remove links from inactive members
    if len(urls) > 0 and member_tup[1] < 20:
        await message.channel.send(f'You do not have permission to send links in this server, {message.author.mention}. You must participate in discussion more before you can send links.')
        await message.delete()

    await bot.process_commands(message)

@bot.command(name='stats')
async def stats(ctx):
    row_tup = fetch_member(ctx.author.id)
    if row_tup == None:
        await ctx.send('You have not sent any messages in this server yet.')
    else:
        plug_access = row_tup[2] > 20
        await ctx.send(f'You have sent {row_tup[1]} messages since I started counting. Plug access: {plug_access}')

@bot.command(name='test')
@commands.has_role('badmin')
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
    cur = con.cursor()

    cur.execute(f'insert into {MEMBER_STATS_TABLE} values ({id}, 1, 0, 0)')
    con.commit()
    cur.close()

def incrememt_message_count(id):
    cur = con.cursor()

    cur.execute(f'update {MEMBER_STATS_TABLE} set {COL_MESSAGE_COUNT} = {COL_MESSAGE_COUNT} + 1 where id = {id}')
    con.commit()
    cur.close()

def add_plug_credit(id):
    cur = con.cursor()
    cur.execute(f'update {MEMBER_STATS_TABLE} set {COL_PLUG_CREDITS} = {COL_PLUG_CREDITS} + 1 where id = {id}')
    con.commit()
    cur.close()

def find_urls(content):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, content)      
    return [x[0] for x in url]


bot.run(sys.argv[1])
