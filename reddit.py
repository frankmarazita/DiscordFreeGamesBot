import os
import ast
import time
import requests

import praw
import bs4
import discord

reddit_credentials = ast.literal_eval(os.getenv('REDDIT_CREDENTIALS'))
reddit = praw.Reddit(**reddit_credentials)
subreddit = reddit.subreddit('freegames')
keywords = ['steam', 'epic', 'gog']

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL = int(os.getenv('DISCORD_CHANNEL'))
client = discord.Client()

def getFreeGames(past_messages):

    to_send = []

    for submission in subreddit.new(limit=10):
        op_text = submission.selftext.lower()
        if any(keyword in submission.url for keyword in keywords):
            send = True
            for message in past_messages:
                if submission.url in message.content:
                    send = False
                    break
            if send:
                title = bs4.BeautifulSoup(requests.get(
                    submission.url).text, features="html.parser").title.text
                send = title + "\n" + submission.url
                to_send.append(send)

    return to_send

@client.event
async def on_ready():
    channel = client.get_channel(DISCORD_CHANNEL)
    while True:
        past_messages = await channel.history(limit=10).flatten()
        for message_to_send in getFreeGames(past_messages):
            await channel.send(message_to_send)

        time.sleep(3600)

client.run(DISCORD_TOKEN)
