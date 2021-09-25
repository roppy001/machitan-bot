# 組み込み
import os
import json
import re
import datetime

# 追加インストール
import discord
import tweepy

# BOT関連
import common
import asyncio

client = discord.Client()
BOT_TOKEN=os.getenv('MACHITAN_BOT_TOKEN')
GUILD_ID=os.getenv('MACHITAN_BOT_GUILD')
CHANNEL_ID=os.getenv('MACHITAN_BOT_CHANNEL')

data = {}

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    
    try:
        data = common.load_data()
    except FileNotFoundError:
        pass

    asyncio.ensure_future(detection_loop())
    return

# 発言時に実行されるイベントハンドラを定義
#@client.event
#async def on_message(message):

async def detection_loop():
    guild = await client.fetch_guild(GUILD_ID)
    channel = await client.fetch_channel(CHANNEL_ID)
    await channel.send('てすとてすと');

    await asyncio.sleep(5)
    asyncio.ensure_future(detection_loop())
    return

# Botの起動とDiscordサーバーへの接続
client.run(BOT_TOKEN)

