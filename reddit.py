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

def getFreeGames(messages):

    to_send = []

    for submission in subreddit.new(limit=10):
        op_text = submission.selftext.lower()
        if any(keyword in submission.url for keyword in keywords):
            posts.append(submission.name)
            title = bs4.BeautifulSoup(requests.get(
                submission.url).text, features="html.parser").title.text
            send = title + "\n" + submission.url
            sent = True
            for message in messages:
                if send == message.content:
                    send = False
                    break
            if send:
                to_send.append(send)

    return to_send

@client.event
async def on_ready():
    channel = client.get_channel(DISCORD_CHANNEL)
    while True:
        messages = await channel.history(limit=10).flatten()
        for message_to_send in getFreeGames(messages):
            await channel.send(message_to_send)

        time.sleep(3600)

client.run(DISCORD_TOKEN)
