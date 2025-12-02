from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    print("Warning: OPENWEATHER_API_KEY not found in environment variables.")

# Initialize FastMCP server
mcp = FastMCP("weather-server")

@mcp.tool()
async def get_weather(location: str, state: str = "") -> str:
    """
    Get the current weather for a specific location (city or village) in India.
    
    Args:
        location: The name of the city or village (e.g., "Hyderabad", "Warangal").
        state: Optional state code or name to help disambiguate (e.g., "Telangana").
    """
    if not API_KEY:
        return "Error: API key not configured."

    query = f"{location},IN"
    if state:
        query = f"{location},{state},IN"

    async with httpx.AsyncClient() as client:
        try:
            # First, get coordinates using Geocoding API
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=1&appid={API_KEY}"
            geo_response = await client.get(geo_url)
            geo_data = geo_response.json()

            if not geo_data:
                return f"Could not find location: {location}"

            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']
            found_name = geo_data[0]['name']
            found_state = geo_data[0].get('state', '')

            # Now get weather data
            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            weather_response = await client.get(weather_url)
            weather_data = weather_response.json()

            description = weather_data['weather'][0]['description']
            temp = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']

            return (
                f"Weather in {found_name}, {found_state}:\n"
                f"Condition: {description.capitalize()}\n"
                f"Temperature: {temp}°C\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} m/s"
            )

        except Exception as e:
            return f"Error fetching weather data: {str(e)}"

if __name__ == "__main__":
    mcp.run()
