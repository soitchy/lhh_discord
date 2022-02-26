# lhh_discord
Repo for the bot that powers the r/LofiHipHop Discord

## Python Dependencies
sqlite3, discord

## TODOS:
 - add error handling lol
 - add a disconnect function to cleanly close the db and whatever
 - add a way for the bot to decrement a member's count if their message is deleted by an admin
 - add a config file so that the hardcoded values in this script can be changed by an admin
 - add some sort of module system to the design so that the bot can be organized
 - add logging
 - add a system for handling beat battles
 - add a system for properly communicating when bepis is pinged (perhaps a model trained from the server itself?)

## Database Info:

 Table "member_stats":
    id: INT PRIMARY KEY -> id refers to the discord unique id
    total_messages: INT NOT NULL
    plug_credits: INT NOT NULL
    feedback_credits: INT NOT NULL

## Creating a test database

