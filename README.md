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
 - add a system for adding roles automatically to users via reactions (like the reaction roles bot)
 - add a system to backup pins in channels to the history channel (like the passel bot)

## Database Info:
```
 Table "member_stats":
    id: INT PRIMARY KEY -> id refers to the discord unique id
    total_messages: INT NOT NULL -> the total number of messages this member has sent
    plug_credits: INT NOT NULL -> the total number of messages over a certain character threshold
    feedback_credits: INT NOT NULL -> currently not used
```
## Creating a test database

Using sqlite3, we will create a test database in a db subdirectory:
```
mkdir db
cd db
sqlite3 lhh.db
```

After running the above, you should be in sqlite's interactive console.

Create the main member stats table:
```
create table member_states (
  id INT PRIMARY KEY NOT NULL,
  total_messages INT NOT NULL,
  plug_credits INT NOT NULL,
  feedback_credits INT NOT NULL
) 
```

You can then quit the interactive console with:
```
quit
```
