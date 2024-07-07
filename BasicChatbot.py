import spacy
import random
import requests

# Load the spaCy model for English
nlp = spacy.load('en_core_web_sm')

# Define intents and responses
intents = {
    "greeting": [
        "Hello! How can I help you today?",
        "Hi there! What can I do for you?",
        "Hey! How's it going?"
    ],
    "goodbye": [
        "Goodbye! Have a great day!",
        "See you later!",
        "Take care!"
    ],
    "how_are_you": [
        "I'm just a bunch of code, but I'm doing well! How about you?",
        "I'm here to help you. How can I assist you today?",
        "Feeling chatty! What can we talk about?"
    ],
    "name": [
        "I'm just a humble chatbot.",
        "I don't have a name, but I'm here to help!",
        "Call me Chatbot. How can I assist?"
    ],
    "weather": [
        "Let me check the weather for you. Please provide a city name."
    ],
    "unknown": [
        "I'm not sure I understand. Could you please rephrase?",
        "Can you clarify that?",
        "I'm here to help, but I didn't get that."
    ]
}


# Function to fetch weather data from OpenWeatherMap API
def get_weather(city_name):
    api_key = '7fd9ee3e184b69503aac9033edafebbe'
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f"The weather in {city_name} is currently {weather_description} with a temperature of {temperature}°C."
        elif response.status_code == 404:
            return "City not found. Please check the city name and try again."
        else:
            return "Failed to retrieve weather information. Please try again later."

    except requests.exceptions.RequestException as e:
        return f"Error: {e}. Please check your internet connection and try again."


# Intent recognition function
def recognize_intent(text):
    doc = nlp(text)
    if any(token.lower_ in ["hi", "hello", "hey"] for token in doc):
        return "greeting"
    elif any(token.lower_ in ["bye", "goodbye", "see you"] for token in doc):
        return "goodbye"
    elif "how" in text.lower() and "you" in text.lower():
        return "how_are_you"
    elif "name" in text.lower():
        return "name"
    elif "weather" in text.lower():
        return "weather"
    else:
        return "unknown"


# Chat function
def chat():
    print("Hi! I'm an advanced chatbot. Type 'quit' to exit.")
    while True:
        user_input = input("You: ").strip().lower()
        if user_input == "quit":
            print("Chatbot: Goodbye!")
            break

        intent = recognize_intent(user_input)
        if intent == "weather":
            print("Chatbot: " + random.choice(intents[intent]))
            city = input("Please provide the city name: ").strip()
            print("Chatbot:", get_weather(city))
        else:
            response = random.choice(intents[intent])
            print("Chatbot:", response)


# Ensure the chat function runs only if this script is executed directly
if __name__ == "__main__":
    chat()
