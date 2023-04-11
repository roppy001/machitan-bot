# 組み込み
import os
import json
import re
import datetime

# 追加インストール
import discord
from discord.ext import tasks
import tweepy

# BOT関連
import common
import asyncio

LOOP_INTERVAL_TIME = 300

BOT_TOKEN=os.getenv('MACHITAN_BOT_TOKEN')
GUILD_ID=os.getenv('MACHITAN_BOT_GUILD')
CHANNEL_ID=os.getenv('MACHITAN_BOT_CHANNEL')
CUNSUMER_KEY=os.getenv('MACHITAN_BOT_CONSUMER_KEY')
CUNSUMER_SECRET=os.getenv('MACHITAN_BOT_CONSUMER_SECRET')
ACCESS_TOKEN=os.getenv('MACHITAN_BOT_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET=os.getenv('MACHITAN_BOT_ACCESS_TOKEN_SECRET')
ROLE_ID=os.getenv('MACHITAN_BOT_ROLE_ID')
QUERY_STR=os.getenv('MACHITAN_BOT_QUERY')
# ループ間隔 デフォルトは10分
LOOP_INTERVAL=os.getenv('MACHITAN_LOOP_INTERVAL', 600)

tweet_auth = tweepy.OAuthHandler(CUNSUMER_KEY, CUNSUMER_SECRET)
tweet_auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweet_api = tweepy.API(tweet_auth)


async def main_loop():
    print(f'Detection start {datetime.datetime.now()}')

    guild = await client.fetch_guild(GUILD_ID)
    channel = await client.fetch_channel(CHANNEL_ID)

    latest_status_id = 0

    data = {}

    try:
        data = common.load_data()
    except FileNotFoundError:
        pass

    if common.LATEST_STATUS_ID_KEY in data:
        latest_status_id = data[common.LATEST_STATUS_ID_KEY]


    tweets = tweepy.Cursor( tweet_api.search_tweets, q=QUERY_STR, since_id=latest_status_id, tweet_mode='extended', result_type="mixed", include_entities=True).items(20)

    strs = []

    fst_flag=True

    for tweet in tweets:
        if fst_flag:
            latest_status_id=tweet.id

            fst_flag=False

        strs.append(f'<@&{ROLE_ID}> \n https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}')

    for s in reversed(strs):
        await channel.send(s)

    data[common.LATEST_STATUS_ID_KEY] = latest_status_id
    
    common.save_data(data)

    print(f'Detection end {datetime.datetime.now()}')
    return

class MainClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        self.background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        #guild = await client.fetch_guild(GUILD_ID)
        #roles = await guild.fetch_roles()

        #print('ロール一覧')
        #for role in roles:
        #    print(f'id={role.id}, name={role.name}')

    @tasks.loop(seconds=LOOP_INTERVAL)  # task runs every 60 seconds
    async def background_task(self):
        await main_loop()

    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

    async def on_message(self, message):
        if message.content in ['.shutdown', '.shutdown_machitan']:
            await client.close()

# Botの起動とDiscordサーバーへの接続
its = discord.Intents.default()
its.message_content = True
client = MainClient(intents=its)
client.run(BOT_TOKEN)

