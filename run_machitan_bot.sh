#!/bin/bash

cd ~/machitan-bot

mkdir log
mkdir data

./run_machitan_bot_1.sh 1>>log/console.log 2>>log/error.txt &

