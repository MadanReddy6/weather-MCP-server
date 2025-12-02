import asyncio
from weather_server import get_weather

# --- EDIT LOCATION HERE ---
LOCATION = "puttaparthi"
STATE = "Andhra Pradesh"  # Optional, leave empty "" if not needed
# --------------------------

async def main():
    print(f"Fetching weather for {LOCATION}...")
    result = await get_weather(LOCATION, STATE)
    print("\n" + result)

if __name__ == "__main__":
    asyncio.run(main())
