#!/usr/bin/env python3

import discord
import os
import requests
import json

my_secret_token = os.environ['TOKEN']
my_jokes_key = os.environ['JOKES_KEY']
my_app_id = os.environ['APP_ID']

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)

def get_quotes():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

def get_jokes():
    api_url = 'https://api.api-ninjas.com/v1/jokes'
    response = requests.get(api_url, headers={'X-Api-Key': my_jokes_key})
    if response.status_code == requests.codes.ok:
        json_data = json.loads(response.text)
        joke = json_data[0]['joke']
        return joke

def get_definition(word):
    api_url = 'https://api.api-ninjas.com/v1/dictionary?word={}'.format(word)
    response = requests.get(api_url, headers={'X-Api-Key': my_jokes_key})
    if response.status_code == requests.codes.ok:
        json_data = json.loads(response.text)
        defnt = json_data['definition']
        if len(defnt) > 2000:
            return defnt[:1980]
        return defnt
    else:
        return "Sorry, I couldn't find that word."

def get_fact():
    api_url = 'https://api.api-ninjas.com/v1/facts'
    response = requests.get(api_url, headers={'X-Api-Key': my_jokes_key})
    if response.status_code == requests.codes.ok:
        json_data = json.loads(response.text)
        fact = json_data[0]['fact']
        return fact

def convert_currency(from_currency, to_currency, amount):
    api_url = f'https://api.api-ninjas.com/v1/convertcurrency?want={to_currency}&have={from_currency}&amount={amount}'
    headers = {'X-Api-Key': my_jokes_key}
    response = requests.get(api_url, headers=headers)

    if response.status_code == requests.codes.ok:
        data = response.json()
        converted_amount = data['new_amount']
        return converted_amount
    else:
        return None

# Modify the get_answer function to handle the response
def get_answer(query):
    url = 'https://www.wolframalpha.com/api/v1/llm-api'
    params = {
            'input': query,
            'appid': '7X9HV7-H4AL64ATEA'
            }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.text.split('Result:')[1].split('Wolfram')[0]
    else:
        return "Cannot proceed your request"



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith('$inspire'):
        quote = get_quotes()
        await message.channel.send(quote)

    elif message.content.startswith('$joke'):
        joke = get_jokes()
        await message.channel.send(joke)

    elif message.content.startswith('$define'):
        word = message.content.split('$define ')[1]
        definition = get_definition(word)
        await message.channel.send(word + ':\n' + definition)

    elif message.content.startswith('$fact'):
        await message.channel.send(get_fact())

    elif message.content.startswith('$ask'):
        answer = get_answer(message.content.split('$ask ')[1])
        await message.channel.send(answer)

    elif message.content.startswith('$currency'):
        amount = message.content.split(' ')[1]
        from_currency = message.content.split(' ')[2]
        to_currency = message.content.split(' ')[3]
        converted_amount = convert_currency(from_currency, to_currency, amount)
        if converted_amount is not None:
            await message.channel.send(f'{amount} {from_currency} = {converted_amount} {to_currency}')
        else:
            await message.channel.send('Sorry, I couldn\'t convert the currency.')

    elif message.content.startswith('$help-currency'):
        await message.channel.send('$currency <amount> <from_currency> <to_currency> - Converts currency!')

    elif message.content.startswith('$help-fact'):
        await message.channel.send('$fact - Tells a fact!')

    elif message.content.startswith('$help-joke'):
        await message.channel.send('$joke - Tells a joke!')

    elif message.content.startswith('$help-define'):
        await message.channel.send('$define <word> - Defines a word!')

    elif message.content.startswith('$help-ask'):
        await message.channel.send('$ask <question> - Asks a question!')

    elif message.content.startswith('$help-currency'):
        await message.channel.send('$currency <amount> <from_currency> <to_currency> - Converts currency!')

    elif message.content.startswith('$help-inspire'):
        await message.channel.send('$inspire - Inspire you!')

    elif message.content.startswith('$help-hello'):
        await message.channel.send('$hello - Hello!')

    elif message.content.startswith('$help'):
        await message.channel.send('$inspire - Inspire you! \n$joke - Tells a joke! \n$define <word> - Defines a word! \n$fact - Tells a fact! \n$ask <question> - Asks a question! \n$currency <amount> <from_currency> <to_currency> - Converts currency!')

    elif message.content.startswith('$commands'):
        await message.channel.send('$inspire\n$joke\n$define\n$fact\n$ask <question>\n$currency <amount> <from_currency> <to_currency>\n$help\n$help-fact\n$help-joke\n$help-define\n$help-ask\n$help-currency\n$help-inspire\n$help-hello')

    else:
        await message.channel.send('Sorry, I do not understand. \nType $help for help')

client.run(my_secret_token)
