import json
from django.core.management.base import BaseCommand
from orders.nova_poshta_service import nova_poshta_service

class Command(BaseCommand):
    help = 'Отримує інформацію про відправника (Counterparty) та контактну особу для налаштування .env'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("=== ОТРИМАННЯ ДАНИХ ДЛЯ НАЛАШТУВАННЯ NOVA POSHTA ==="))

        # 1. Отримуємо Counterparty (Відправника)
        self.stdout.write("\n1. Шукаємо Sender (CounterpartyRef)...")
        senders = nova_poshta_service.get_senders()
        
        if not senders:
            self.stdout.write(self.style.ERROR("❌ Не знайдено жодного відправника. Перевірте API Key."))
            return

        for idx, sender in enumerate(senders):
            self.stdout.write(f"\n[{idx+1}] Відправник: {sender.get('Description')} (Ref: {sender.get('Ref')})")
            self.stdout.write(f"    CityRef: {sender.get('City')}")
            
            # 2. Для кожного відправника шукаємо контактних осіб
            self.stdout.write(f"    --> Шукаємо контактних осіб...")
            contacts = nova_poshta_service.get_sender_contact(sender.get('Ref'))
            
            for c_idx, contact in enumerate(contacts):
                self.stdout.write(f"       [{c_idx+1}] {contact.get('Description')} | Phone: {contact.get('Phones')} | Ref: {contact.get('Ref')}")

            # 3. Шукаємо адреси відправника (Склади/Відділення)
            self.stdout.write(f"    --> Шукаємо адреси (Склади) для відправника...")
            addresses = nova_poshta_service.get_sender_addresses(sender.get('Ref'))
            for a_idx, addr in enumerate(addresses):
                self.stdout.write(f"       [{a_idx+1}] {addr.get('Description')} (CityRef: {addr.get('CityRef')})")
                self.stdout.write(f"           AddressRef: {addr.get('Ref')}")

        self.stdout.write(self.style.SUCCESS("\n[OK] Скопіюйте потрібні Ref у ваш .env файл:"))
        self.stdout.write("NOVA_POSHTA_SENDER_REF=...")
        self.stdout.write("NOVA_POSHTA_SENDER_CITY_REF=...")
        self.stdout.write("NOVA_POSHTA_SENDER_ADDRESS_REF=... (Це Ref вашого складу/відділення)")
        self.stdout.write("NOVA_POSHTA_SENDER_CONTACT_REF=...")
        self.stdout.write("NOVA_POSHTA_SENDER_PHONE=...")
