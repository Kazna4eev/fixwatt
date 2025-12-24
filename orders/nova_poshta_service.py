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


    def get_senders(self):
        """Отримати список контрагентів (Senders)."""
        response = self._make_request(
            modelName="Counterparty",
            calledMethod="getCounterparties",
            methodProperties={"CounterpartyProperty": "Sender"}
        )
        if response.get('success'):
            return response.get('data', [])
        return []

    def get_sender_contact(self, sender_ref):
        """Отримати контактних осіб контрагента."""
        response = self._make_request(
            modelName="Counterparty",
            calledMethod="getCounterpartyContactPersons",
            methodProperties={"Ref": sender_ref}
        )
        if response.get('success'):
            return response.get('data', [])
        return []

    def get_sender_addresses(self, sender_ref):
        """Отримати адреси контрагента."""
        response = self._make_request(
            modelName="Counterparty",
            calledMethod="getCounterpartyAddresses",
            methodProperties={"Ref": sender_ref, "CounterpartyProperty": "Sender"}
        )
        if response.get('success'):
            return response.get('data', [])
        return []

    def get_or_create_recipient(self, phone, first_name, last_name, email=''):
        """
        Знаходить або створює отримувача (Counterparty).
        Повертає словник {counterparty_ref, contact_ref} або None.
        """
        properties = {
            "CounterpartyProperty": "Recipient",
            "Phone": phone,
            "Email": email,
            "LastName": last_name,
            "FirstName": first_name,
            "CounterpartyType": "PrivatePerson"
        }

        response = self._make_request(
            modelName="Counterparty",
            calledMethod="save",
            methodProperties=properties
        )

        if response.get('success') and response.get('data'):
            data = response['data'][0]
            # API повертає Ref контрагента. Також зазвичай там є ContactPerson.
            counterparty_ref = data['Ref']
            
            # Нам також потрібен ContactPerson Ref (зазвичай створюється автоматично разом з контрагентом)
            # У відповіді може бути field 'ContactPerson' -> 'data' -> [0] -> 'Ref'
            # Але структура відповіді 'save' для Counterparty може відрізнятися.
            # Надійніше отримати контакти окремим запитом, якщо їх немає у відповіді.
            
            contact_ref = None
            if 'ContactPerson' in data and data['ContactPerson'].get('data'):
                 contact_ref = data['ContactPerson']['data'][0]['Ref']
            else:
                # Якщо не повернуло контакт, шукаємо його вручну
                contacts = self.get_sender_contact(counterparty_ref) # Цей метод підходить і для отримувачів
                if contacts:
                    contact_ref = contacts[0]['Ref']

            return {
                'recipient_ref': counterparty_ref,
                'contact_ref': contact_ref
            }
            
        return None

    def create_waybill(self, order, sender_config):
        """
        Створення експрес-накладної.
        """
        # 1. Знаходимо/Створюємо отримувача
        recipient_info = self.get_or_create_recipient(
            phone=order.phone,
            first_name=order.first_name,
            last_name=order.last_name,
            email=order.email
        )
        
        if not recipient_info or not recipient_info['contact_ref']:
             return {'success': False, 'errors': ['Не вдалося створити отримувача (Recipient/Contact). Перевірте телефон/ПІБ.']}

        # Дата відправки - сьогодні
        import datetime
        date_str = datetime.datetime.now().strftime("%d.%m.%Y")
        
        # Вага - поки що ставимо 1 кг за замовчуванням
        weight = "1"
        
        # Об'єм в кубах (0.004 = 20x20x10см приблизно)
        volume_general = "0.004"

        properties = {
            "PayerType": "Recipient",        # Платить отримувач
            "PaymentMethod": "Cash",         # Готівка
            "DateTime": date_str,            # Дата відправки
            "CargoType": "Parcel",           # Посилка
            "VolumeGeneral": volume_general, 
            "Weight": weight,
            "ServiceType": "WarehouseWarehouse", # Відділення-Відділення
            "SeatsAmount": "1",              # Кількість місць
            "Description": f"Замовлення {order.id}",
            "Cost": str(max(order.get_total_cost(), 200)), # Оціночна вартість (мінімум 200)

            # --- ВІДПРАВНИК ---
            "CitySender": sender_config['city_ref'],
            "Sender": sender_config['sender_ref'],
            "SenderAddress": sender_config['address_ref'],
            "ContactSender": sender_config['contact_ref'],
            "SendersPhone": sender_config['phone'],

            # --- ОТРИМУВАЧ ---
            "CityRecipient": order.city_ref,
            "RecipientAddress": order.warehouse_ref,
            "Recipient": recipient_info['recipient_ref'], # <--- ДОДАНО Ref
            "ContactRecipient": recipient_info['contact_ref'], # <--- ДОДАНО Ref
            "RecipientName": f"{order.last_name} {order.first_name}",
            "RecipientType": "PrivatePerson",
            "RecipientsPhone": order.phone,
        }

        response = self._make_request(
            modelName="InternetDocument",
            calledMethod="save",
            methodProperties=properties
        )

        if response.get('success'):
            # Повертаємо Ref накладної та номер накладної (IntDocNumber)
            data = response['data'][0]
            return {
                'success': True,
                'ttn': data['IntDocNumber'],
                'ref': data['Ref'],
                'cost': data['CostOnSite']
            }
        else:
            errors = response.get('errors', [])
            return {'success': False, 'errors': errors}

nova_poshta_service = NovaPoshtaService()