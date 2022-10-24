import os
from dotenv import load_dotenv

load_dotenv()

# Api settings
key = os.getenv('API_KEY')   # Use .format to replace the values
supported_countries = 'http://api.airvisual.com/v2/countries?key={KEY}'
states_in_country = 'http://api.airvisual.com/v2/states?country={COUNTRY_NAME}&key={KEY}'
cities_in_state = 'http://api.airvisual.com/v2/cities?state={STATE_NAME}&country={COUNTRY_NAME}&key={KEY}'
city_data_IP = 'http://api.airvisual.com/v2/nearest_city?key={KEY}'
city_data_GPS = 'http://api.airvisual.com/v2/nearest_city?lat={LATITUDE}&lon={LONGITUDE}&key={KEY}'
spec_city_data = 'http://api.airvisual.com/v2/city?city={CITY}&state={STATE}&country={COUNTRY}&key={KEY}'

# App Screen settings
WIDTH = 1500
HEIGHT = 900

# DB Settings
DATABASE_NAME = os.getenv('DATABASE_NAME', 'air_quality')
DATABASE_USER = os.getenv('DATABASE_USER', 'root')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'root')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
