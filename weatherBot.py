import json
import os
import random
import discord
import requests
from dotenv import load_dotenv

current_weather_url = "https://api.openweathermap.org/data/2.5/weather"
forecast_weather_url = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = "8d00b786d6ffb3f20b16837837070c3b"

def get_current_weather(city):
    url = f"{current_weather_url}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    status = response.status_code
    if status == 200:
        response = json.loads(response.text)
        return response, status
    else:
        return response.text, status

def get_weather_forecast(city):
    url = f"{forecast_weather_url}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    status = response.status_code
    if status == 200:
        response = json.loads(response.text)
        return response, status
    else:
        return response.text, status

def get_weather_advice(temp):
    if temp < 0:
        return "It's freezing! Make sure to wear a thick coat, gloves, and a hat."
    elif temp < 10:
        return "It's pretty cold. Don't forget to wear a jacket!"
    elif temp < 20:
        return "It's a bit chilly. A light jacket should be enough."
    elif temp < 30:
        return "The weather is nice. You can go out in a t-shirt."
    else:
        return "It's hot! Stay cool and drink plenty of water."

weather_jokes = [
    "Why did the woman go outdoors with her purse open? Because she expected some change in the weather!",
    "What does a cloud wear under his raincoat? Thunderwear.",
    "What’s the difference between weather and climate? You can’t weather a tree, but you can climate.",
    "What’s a tornado’s favorite game to play? Twister!"
]

def get_food_suggestions(temp):
    if temp < 0:
        return "How about some hot chocolate or a warm bowl of soup?"
    elif temp < 10:
        return "A hot coffee or a nice stew would be perfect!"
    elif temp < 20:
        return "Maybe a warm sandwich or a cup of tea?"
    elif temp < 30:
        return "A fresh salad or a cold beverage sounds great!"
    else:
        return "How about some ice cream or a cold smoothie?"

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == 'hi':
        await message.channel.send(f"Hello, {message.author.name}! I am a Weather Bot made by group K1 for Cloud Computing Project.")
    elif message.content.lower().startswith('how are you'):
        await message.channel.send("I am fine! Thank You!")
    elif message.content.lower().startswith('who are you'):
        await message.channel.send("Welcome to drizzle, the ultimate weather companion for your Discord server! Whether you're planning a trip, curious about today's weather, or just want some fun interactions, drizzle has got you covered.")
    elif message.content.lower() == '!help':
        await message.channel.send("I am a Weather Bot made by group K1 for Cloud Computing Project.")
        await message.channel.send("Commands you can use:")
        await message.channel.send("!current <city> -- Get the current weather information for the city.")
        await message.channel.send("!tomorrow <city> -- Get the weather forecast for tomorrow for the city.")
        await message.channel.send("!forecast <city> -- Get the weather forecast for the next 5 days for the city.")
        await message.channel.send("!compare <city1> <city2> -- Compare the weather between two cities.")
        await message.channel.send("!advice <city> -- Get advice on what to wear based on the current temperature.")
        await message.channel.send("!food <city> -- Get food suggestions based on the current temperature.")
        await message.channel.send("!joke -- Hear a weather-related joke.")
    
    elif message.content.startswith('!current '):
        city = message.content[9:]
        info, status = get_current_weather(city)
        if status == 200:
            await message.channel.send(f"Current weather data for {city.title()}:")
            await message.channel.send(f"Temperature: {info['main']['temp']}°C")
            await message.channel.send(f"Feels like: {info['main']['feels_like']}°C")
            await message.channel.send(f"Minimum Temperature: {info['main']['temp_min']}°C")
            await message.channel.send(f"Maximum Temperature: {info['main']['temp_max']}°C")
            await message.channel.send(f"Humidity: {info['main']['humidity']}%")
            await message.channel.send(f"Wind Speed: {info['wind']['speed']} m/s")
            await message.channel.send(f"Weather: {info['weather'][0]['description']}")
        else:
            await message.channel.send(f"Error fetching data for {city.title()}: {info}")

    elif message.content.startswith('!tomorrow '):
        city = message.content[10:]
        info, status = get_weather_forecast(city)
        if status == 200:
            tomorrow = info['list'][8]
            await message.channel.send(f"Weather forecast for tomorrow in {city.title()}:")
            await message.channel.send(f"Temperature: {tomorrow['main']['temp']}°C")
            await message.channel.send(f"Weather: {tomorrow['weather'][0]['description']}")
        else:
            await message.channel.send(f"Error fetching data for {city.title()}: {info}")

    elif message.content.startswith('!forecast '):
        city = message.content[10:]
        info, status = get_weather_forecast(city)
        if status == 200:
            await message.channel.send(f"5-day weather forecast for {city.title()}:")
            for forecast in info['list']:
                date = forecast['dt_txt']
                temp = forecast['main']['temp']
                weather = forecast['weather'][0]['description']
                await message.channel.send(f"Date: {date}, Temperature: {temp}°C, Weather: {weather}")
        else:
            await message.channel.send(f"Error fetching forecast for {city.title()}: {info}")

    elif message.content.startswith('!compare '):
        cities = message.content[9:].split()
        if len(cities) == 2:
            city1, city2 = cities
            info1, status1 = get_current_weather(city1)
            info2, status2 = get_current_weather(city2)
            if status1 == 200 and status2 == 200:
                await message.channel.send(f"Weather comparison for {city1.title()} and {city2.title()}:")
                await message.channel.send(f"{city1.title()} - Temperature: {info1['main']['temp']}°C, Humidity: {info1['main']['humidity']}%, Wind Speed: {info1['wind']['speed']} m/s, Weather: {info1['weather'][0]['description']}")
                await message.channel.send(f"{city2.title()} - Temperature: {info2['main']['temp']}°C, Humidity: {info2['main']['humidity']}%, Wind Speed: {info2['wind']['speed']} m/s, Weather: {info2['weather'][0]['description']}")
            else:
                await message.channel.send("Error fetching data for one or both cities. Please make sure the city names are correct.")
        else:
            await message.channel.send("Please provide exactly two city names for comparison.")

    elif message.content.startswith('!advice '):
        city = message.content[8:]
        info, status = get_current_weather(city)
        if status == 200:
            temp = info['main']['temp']
            advice = get_weather_advice(temp)
            await message.channel.send(f"The current temperature in {city.title()} is {temp}°C.")
            await message.channel.send(advice)
        else:
            await message.channel.send(f"Error fetching data for {city.title()}: {info}")

    elif message.content.startswith('!food '):
        city = message.content[6:]
        info, status = get_current_weather(city)
        if status == 200:
            temp = info['main']['temp']
            food_suggestion = get_food_suggestions(temp)
            await message.channel.send(f"The current temperature in {city.title()} is {temp}°C.")
            await message.channel.send(food_suggestion)
        else:
            await message.channel.send(f"Error fetching data for {city.title()}: {info}")

    elif message.content.lower() == '!joke':
        joke = random.choice(weather_jokes)
        await message.channel.send(joke)

client.run(TOKEN)
