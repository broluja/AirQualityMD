import requests

from Controller.config import (
    key, supported_countries, states_in_country, cities_in_state, spec_city_data, city_data_IP)
from Controller.exceptions import *


class APIManager:
    """API client for retrieving data from the source."""
    statuses = {
        'Call Limit Reached': CallLimitReachedException,
        'Api Key Expired': ApiKeyExpiredException,
        'Incorrect Api Key': IncorrectApiKeyException,
        'Ip Location Failed': IpLocationFailedException,
        'No Nearest Station': NoNearestLocationException,
        'Feature Not Available': FeatureNotAvailableException,
        'Too Many Requests': TooManyRequestsException,
        'Forbidden': ForbiddenException,
        "permission_denied (you don't have access to this endpoint": PermissionDeniedException
    }

    def __init__(self):
        self.key = key

    def get_countries(self) -> list:
        """
        Getting the list of available countries

        Returns:
            list: return a list of countries
        """
        url = supported_countries.format(KEY=self.key)
        data = requests.get(url).json()
        if data.get('status') != 'success':
            raise self.statuses.get(data['data']['message'], APIException)
        countries = [list(country.values())[0] for country in data.get('data')]
        countries.insert(0, 'Serbia')
        return countries

    def get_states(self, country: str) -> list:
        """
        Getting the list of states within given country.
        Args:
            country: name of the country
        Returns:
            list: states within a country
        """
        url = states_in_country.format(COUNTRY_NAME=country, KEY=self.key)
        data = requests.get(url).json()
        if data.get('status') == 'success':
            return [list(state.values())[0] for state in data.get('data')]
        else:
            raise self.statuses.get(data['data']['message'], APIException)

    def get_cities(self, country: str, state: str) -> list:
        """
        Getting the list of cities within a given country and state
        Args:
            country: name of the country
            state: name of the state
        Returns:
            list: cities within the state and country
        """
        url = cities_in_state.format(STATE_NAME=state, COUNTRY_NAME=country, KEY=self.key)
        data = requests.get(url).json()
        if data.get('status') == 'success':
            return [list(city.values())[0] for city in data.get('data')]
        else:
            raise self.statuses.get(data['data']['message'], APIException)

    def get_city_data(self, city: str, state: str, country: str) -> dict:
        """
        Getting the data for given city in a country and state
        Args:
            city: name of the city
            state: name of the state
            country: name of the country
        Returns:
            dictionary: pollution data
        """
        url = spec_city_data.format(CITY=city, STATE=state, COUNTRY=country, KEY=self.key)
        data = requests.get(url).json()
        if data.get('status') == 'success':
            return data['data']['current']
        else:
            raise self.statuses.get(data['data']['message'], APIException)

    def get_nearest_city(self) -> dict:
        """
        Getting data for the nearest city in your location.
        Returns:
            dictionary: data for the nearest city
        """
        url = city_data_IP.format(KEY=self.key)
        data = requests.get(url).json()
        if data.get('status') == 'success':
            return data['data']
        else:
            raise self.statuses.get(data['data']['message'])
