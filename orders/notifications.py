from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_order_confirmation_email(order):
    """
    Відправляє email-підтвердження клієнту та сповіщення адміністратору.
    """
    # --- Лист для клієнта ---
    subject_customer = f"Підтвердження замовлення №{order.id}"
    from_email = 'noreply@fixwatt.com'
    to_customer = order.email

    html_content = render_to_string('orders/email/order_notification_customer.html', {'order': order})

    msg_customer = EmailMultiAlternatives(subject_customer, body="Дякуємо за ваше замовлення!", from_email=from_email,
                                          to=[to_customer])
    msg_customer.attach_alternative(html_content, "text/html")

    # --- Лист для адміністратора ---
    subject_admin = f"Нове замовлення №{order.id} на сайті"
    to_admin = ['your-admin-email@example.com']  # Вкажіть вашу пошту адміністратора

    text_content_admin = render_to_string('orders/email/order_notification_admin.txt', {'order': order})

    msg_admin = EmailMultiAlternatives(subject_admin, body=text_content_admin, from_email=from_email, to=to_admin)

    try:
        msg_customer.send()
        msg_admin.send()
        print(f"Сповіщення для замовлення №{order.id} успішно 'відправлено' в консоль.")
    except Exception as e:
        print(f"Помилка при відправці email: {e}")