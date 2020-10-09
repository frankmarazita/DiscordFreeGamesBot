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
keywords = ['steam', 'epic']

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL = int(os.getenv('DISCORD_CHANNEL'))
client = discord.Client()

posts = []

def getFreeGames():

    messages = []

    for submission in subreddit.new(limit=10):
        op_text = submission.selftext.lower()
        if submission.name not in posts:
            if any(keyword in submission.url for keyword in keywords):
                posts.append(submission.name)
                title = bs4.BeautifulSoup(requests.get(
                    submission.url).text, features="html.parser").title.text
                messages.append(title + "\n" + submission.url)

    return messages

@client.event
async def on_ready():
    channel = client.get_channel(DISCORD_CHANNEL)
    while True:
        for message in getFreeGames():
            await channel.send(message)

        time.sleep(3600)

client.run(DISCORD_TOKEN)
