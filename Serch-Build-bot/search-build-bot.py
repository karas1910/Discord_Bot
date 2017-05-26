import json
import requests
from lxml import html
import discord
import logging
import urllib
import config
from bs4 import BeautifulSoup


client = discord.Client()


@client.event
async def on_ready():
    print('起動しました!')
    print('ユーザーネーム: {}  ユーザーID: {}'.format(client.user.name, client.user.id))


@client.event
async def on_message(message):
    if message.content.startswith('!build') and client.user.id != message.author.id:
        try:
            champion, role = message.content.split()[1:]
        except:
            await client.send_message(message.channel, '!build [champion] [top|jungle|middle|adc|support]')
        else:
            champion = champion[0].upper() + champion[1:].lower()
            if role.upper() == 'ADC':
                role = role.upper()
            else:
                role = role[0].upper() + role[1:].lower()
            try:
                item_build = fetch_build(champion, role)
            except:
                await client.send_message(message.channel, 'Unknown build combination or error fetching request.')
            else:
                await client.send_message(message.channel, item_build)
        print("投稿者：", message.author, "メッセージ：", message.content)
    elif message.content.startswith('!ping'):
        await client.send_message(message.channel, 'pong')


def fetch_build(champion, role):
    try:
        r = 'http://champion.gg/champion/{}/{}'.format(champion, role)
    except requests.exceptions.HTTPError:
        return None
    else:
        html = urllib.request.urlopen(r)
        soup = BeautifulSoup(html, "lxml")
        tables = soup.findAll('div', class_='build-wrapper')
        a = tables[0].findAll('a')
        item_build = []
        for i in a:
            item_build.append(i.attrs['href'].split('/')[-1])

        return item_build


client.run(config.TOKEN_ID)
