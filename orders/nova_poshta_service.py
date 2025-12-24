import requests
from django.conf import settings


class NovaPoshtaService:
    """
    Сервіс для роботи з реальним API Нової Пошти.
    Використовує робочий метод getCities.
    """

    API_URL = "https://api.novaposhta.ua/v2.0/json/"

    def __init__(self):
        self.api_key = settings.NOVA_POSHTA_API_TOKEN

    def _make_request(self, modelName, calledMethod, methodProperties=None):
        """Відправляє запит до API."""
        if not self.api_key:
            return {'data': [], 'success': False}

        payload = {
            "apiKey": self.api_key,
            "modelName": modelName,
            "calledMethod": calledMethod,
            "methodProperties": methodProperties or {}
        }

        try:
            response = requests.post(self.API_URL, json=payload, timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Помилка API НП: {e}")
            return {'data': [], 'success': False}

    def get_cities(self, term=''):
        """
        Отримує список міст через метод getCities (який у вас працює!).
        """
        method_properties = {
            "FindByString": term,  # Цей параметр працює з getCities
            "Limit": "20"
        }

        response = self._make_request(
            modelName="Address",
            calledMethod="getCities",  # <--- ВИКОРИСТОВУЄМО РОБОЧИЙ МЕТОД
            methodProperties=method_properties
        )

        if response.get('success') and response.get('data'):
            # Формат відповіді getCities трохи простіший: data - це одразу список міст
            cities = []
            for city in response['data']:
                # Використовуємо 'Ref' та 'Description' (українська назва)
                cities.append((city['Ref'], city['Description']))
            return cities

        return []

    def get_warehouses(self, city_ref, term=''):
        """
        Отримує відділення для міста. Цей метод зазвичай працює у всіх.
        """
        method_properties = {
            "CityRef": city_ref,
            "Limit": "500",  # Завантажуємо більше відділень
            "Language": "UA"
        }

        # Якщо є пошуковий термін для відділення, додаємо його
        if term:
            method_properties["FindByString"] = term

        response = self._make_request(
            modelName="Address",
            calledMethod="getWarehouses",
            methodProperties=method_properties
        )

        if response.get('success') and response.get('data'):
            return [(wh['Ref'], wh['Description']) for wh in response['data']]

        return []


nova_poshta_service = NovaPoshtaService()