
import streamlit as st
import requests
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Set API Keys
GOOGLE_API_KEY = "AIzaSyDvmhpLuwIzaegbN9Zm2x7ArOsHkGkcljY"
OPENWEATHER_API_KEY = "f8a444244309ec***0f14b701603e86b"

# Configure Google Gemini Model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)

# Create Prompt Template
prompt = PromptTemplate(
    input_variables=["city", "weather", "temperature", "humidity", "description"],
    template="""The current weather in {city} is {description}.
    The temperature is {temperature}°C with {humidity}% humidity.
    {weather}. Provide a simple, friendly response.
    """
)

# New LangChain format (RunnableSequence)
chain = prompt | llm

# Function to Get Weather Data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        return None
    
    return {
        "city": city,
        "weather": response["weather"][0]["main"],
        "temperature": response["main"]["temp"],
        "humidity": response["main"]["humidity"],
        "description": response["weather"][0]["description"].capitalize()
    }

# Streamlit UI
st.title("🌦️ AI-Powered Weather App")

city = st.text_input("Enter a city name:", "")

if st.button("Get Weather"):
    if city:
        weather_data = get_weather(city)
        if weather_data:
            response = chain.invoke(weather_data)  # Call Gemini AI
            st.success(response.content)  # Extract and display content
        else:
            st.error("City not found. Please enter a valid city.")
    else:
        st.warning("Please enter a city name.")
