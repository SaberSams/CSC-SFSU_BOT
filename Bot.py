from dotenv import load_dotenv
from os import getenv
import discord

# $pip install "pymongo[srv]"
from pymongo import MongoClient

# $ pip install alt-profanity-check
# $ pip install scikit-learn==0.20.2
from better_profanity import profanity

# load .env file
load_dotenv() 

# load the Database
print("Loading Database")
db_name = getenv('DB_NAME')
db_pw = getenv("DB_PW")
db_url = getenv("DB_URL")
db_client = MongoClient(f"mongodb+srv://{db_name}:{db_pw}@{db_url}")
db = db_client.discord

# load the Bot
print("Loading Bot")
bot = discord.Client()
token = getenv("DISCORD_API_TOKEN")


async def strike(user_id):
    pass


# run when bot connects to a server 
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to discord')


# run on every message
@bot.event
async def on_message(message):
    author_id = message.author.id

    # Keep the bot from checking its own messages.
    if author_id is bot.user.id:
        return

    # Check if this author has an account
    account = db.accounts.find_one({"user_id": author_id})
    print(account)
    # If there is no account create one.
    if account is None:
        db.accounts.insert_one({
            "user_id":author_id,
            "strikes": {
                f"{message.guild.id}":0,
            },
            "swag":0})
        print(f"Account created for {message.author.name}")

    # Check for Profanity, this isnt a very good lib but I couln't get profanity-check to work.
    if profanity.contains_profanity(message.content):
        db.accounts.update_one(
            {"user_id":author_id},
            {"$inc": {f"strikes.{message.guild.id}":1}},
            upsert=True
        )

       
#async def swag(message):

    # if the incoming message wasnt sent by the bot
    #if isNotOurMessage and "swag" in message.content:
    #    senderID = message.author.id

     #   if (senderID in self.profiles):
      #      profiles[senderID].strikes += 1        # if we have a profile on this user, edit existing values
       # else:
        #    profiles[senderID] = UserProfile()     # else, create a profile for them

    #    swagEmoji = ":moneybag:"

    #    for i in range(self.profiles[senderID].strikes):
    #        swagEmoji *= 2

    #   await message.channel.send(swagEmoji)


bot.run(token)
