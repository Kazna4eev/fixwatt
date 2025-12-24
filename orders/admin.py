from django.contrib import admin, messages
from .models import Order, OrderItem

# --- ФУНКЦІЯ-ДІЯ (Генерація ТТН) ---
@admin.action(description='Згенерувати ТТН для обраних')
def generate_ttn_action(modeladmin, request, queryset):
    count = 0
    for order in queryset:
        if order.ttn:
            
            continue
            
        try:
            # === ТУТ БУДЕ ПІДКЛЮЧЕННЯ ДО API НОВОЇ ПОШТИ ===
            # Поки що ми генеруємо "фейковий" номер для тесту логіки
            fake_ttn = f"204500{order.id}9999" 
            
            order.ttn = fake_ttn
            order.status = 'shipped' 
            order.save()
            count += 1
        except Exception as e:
            modeladmin.message_user(request, f"Помилка з замовленням {order.id}: {e}", level=messages.ERROR)

    
    if count > 0:
        modeladmin.message_user(request, f"Успішно створено ТТН для {count} замовлень!", level=messages.SUCCESS)
    else:
        modeladmin.message_user(request, "Не оновлено жодного замовлення (можливо, ТТН вже існують).", level=messages.WARNING)


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