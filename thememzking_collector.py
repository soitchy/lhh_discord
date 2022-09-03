import discord
import pandas as pd
import random

quotes_file = open("lhh_discord/thememzking_quotes.csv", "a")

thememzking_id = 410169704338948096

client = discord.Client()

@client.event
async def on_message(msg):
    if msg.author.id == thememzking_id:  # if from thememzking
        await add_to_df(msg)

def add_to_df(msg):
    quotes_file.writerow(msg)

def return_quote():
    quotes_file_list = list(quotes_file)
    nums_of_rows = len(quotes_file.index)
    rnum = random.randint(1, nums_of_rows)

    rand_quote = quotes_file_list.index(rnum)

    return '"' + rand_quote + '" - ㄒ卄乇爪乇爪乙Ҝ丨几Ꮆ'