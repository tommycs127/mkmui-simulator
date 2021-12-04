import discord
import random

client = discord.Client()

reply_simple = [
    '哦',
    '嗯',
]

reply_combinable = [
    '收皮啦',
    '食屎啦',
    '關我咩事呢',
    '關你咩事呢',
    '瞓啦',
]

reply_suffix = [
    '毒撚',
    '毒L',
    '柒頭',
    '7頭',
    '仆街',
    'on9',
]

reply_emoji = [
    '7.7',
    '7.777',
    '：）',
    '：（',
]

reply_sticker = [
    None
]


@client.event
async def on_ready():
    print('{0.user}駕到！'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$娘娘'):
        final_message = ''
        if random.randint(0,2):
            final_message += random.choice(reply_combinable)
            if random.randint(0,2):
                final_message += random.choice(reply_suffix)
        else:
            final_message += random.choice(reply_simple)
        if random.randint(0,1):
            if random.randint(0,1):
                final_message += random.choice(reply_emoji)
            else:
                final_message += random.choice(reply_sticker) or ''
        
        await message.channel.send(final_message)

client.run('Put your token here la 7.7')