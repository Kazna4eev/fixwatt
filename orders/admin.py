from django.contrib import admin, messages
from .models import Order, OrderItem
from django.conf import settings

# --- ФУНКЦІЯ-ДІЯ (Генерація ТТН) ---
@admin.action(description='Згенерувати ТТН для обраних')
def generate_ttn_action(modeladmin, request, queryset):
    count = 0
    for order in queryset:
        if order.ttn:
            
            continue
            
        # Перевірка наявності даних отримувача
        if not order.city_ref or not order.warehouse_ref:
            modeladmin.message_user(request, f"Замовлення {order.id}: Відсутні дані про доставку (CityRef/WarehouseRef).", level=messages.ERROR)
            continue

        # Збираємо конфіг відправника з settings
        sender_config = {
            'sender_ref': settings.NOVA_POSHTA_SENDER_REF,
            'city_ref': settings.NOVA_POSHTA_SENDER_CITY_REF,
            'address_ref': settings.NOVA_POSHTA_SENDER_ADDRESS_REF,
            'contact_ref': settings.NOVA_POSHTA_SENDER_CONTACT_REF,
            'phone': settings.NOVA_POSHTA_SENDER_PHONE
        }

        # Перевіряємо чи налаштовано відправника
        if not all(sender_config.values()):
            modeladmin.message_user(request, "Не налаштовано дані відправника в settings.py!", level=messages.ERROR)
            return

        try:
            from .nova_poshta_service import nova_poshta_service
            
            result = nova_poshta_service.create_waybill(order, sender_config)
            
            if result['success']:
                order.ttn = result['ttn']
                order.status = 'shipped'
                order.save()
                count += 1
            else:
                 error_msg = "; ".join(result.get('errors', []))
                 modeladmin.message_user(request, f"Помилка НП для {order.id}: {error_msg}", level=messages.ERROR)

        except Exception as e:
            modeladmin.message_user(request, f"Помилка з замовленням {order.id}: {e}", level=messages.ERROR)

    if count > 0:
        modeladmin.message_user(request, f"Успішно створено ТТН для {count} замовлень!", level=messages.SUCCESS)
    else:
        modeladmin.message_user(request, "Процес завершено.", level=messages.INFO)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    readonly_fields = ['price'] 
    extra = 0 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'user', 'first_name', 'last_name', 'phone', 
                    'city_name', 'status', 'ttn', 'paid', 'created']
    
    list_filter = ['status', 'paid', 'created', 'updated']
    
    list_editable = ['paid', 'status']
    
    
    search_fields = ['last_name', 'email', 'phone', 'ttn']
    
    inlines = [OrderItemInline]
    
    
    actions = [generate_ttn_action]