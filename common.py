import json

import discord


#class CommandError(Exception):
#    pass

LATEST_STATUS_ID_KEY = 'latest_status_id'

DATA_PATH = 'data/data.txt'

# 日次予約情報を読み込む
def load_data():
    fp = open(DATA_PATH, 'r', encoding="utf-8")

    data =json.load(fp)

    fp.close()

    return data

# 日次予約情報を書き込む
def save_data(data):
    fp = open(DATA_PATH, 'w', encoding="utf-8")

    json.dump(data, fp, indent=4)

    fp.close()

    return

# ロックファイルを生成 失敗した場合はエラー
#def create_lock():
#    fp = open(DATA_LOCK_PATH, 'x', encoding="utf-8")
#    fp.close()

