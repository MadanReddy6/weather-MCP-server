import unittest
from unittest.mock import patch, AsyncMock
import asyncio
from weather_server import get_weather

class TestWeatherServer(unittest.TestCase):
    @patch('weather_server.API_KEY', 'test_api_key')
    @patch('httpx.AsyncClient')
    def test_get_weather_success(self, mock_client_cls):
        # Mock the async client and responses
        mock_client = AsyncMock()
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        # Mock Geocoding API response
        mock_geo_response = AsyncMock()
        mock_geo_response.json.return_value = [{
            'lat': 17.3850,
            'lon': 78.4867,
            'name': 'Hyderabad',
            'state': 'Telangana'
        }]
        
        # Mock Weather API response
        mock_weather_response = AsyncMock()
        mock_weather_response.json.return_value = {
            'weather': [{'description': 'clear sky'}],
            'main': {'temp': 25.5, 'humidity': 60},
            'wind': {'speed': 3.5}
        }

        # Set up side_effect for client.get to return different responses
        mock_client.get.side_effect = [mock_geo_response, mock_weather_response]

        # Run the function
        result = asyncio.run(get_weather("Hyderabad"))

        # Verify result
        self.assertIn("Hyderabad", result)
        self.assertIn("Telangana", result)
        self.assertIn("Clear sky", result)
        self.assertIn("25.5°C", result)

    @patch('weather_server.API_KEY', 'test_api_key')
    @patch('httpx.AsyncClient')
    def test_get_weather_location_not_found(self, mock_client_cls):
        mock_client = AsyncMock()
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        mock_geo_response = AsyncMock()
        mock_geo_response.json.return_value = [] # Empty list means not found
        mock_client.get.return_value = mock_geo_response

        result = asyncio.run(get_weather("UnknownPlace"))
        self.assertIn("Could not find location", result)

if __name__ == '__main__':
    unittest.main()
