# 組み込み
import os
import json
import re
import datetime

# 追加インストール
import discord
import tweepy

client = discord.Client()

BOT_TOKEN=os.getenv('MACHITAN_BOT_TOKEN')


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    return

# 発言時に実行されるイベントハンドラを定義
@client.event
async def on_message(message):
    return

# Botの起動とDiscordサーバーへの接続
client.run(BOT_TOKEN)