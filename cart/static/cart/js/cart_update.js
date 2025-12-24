$(document).ready(function() {

    // 1. ЛОГІКА ОНОВЛЕННЯ КІЛЬКОСТІ (як було раніше)
    // Ми використовуємо подію 'change' на полях quantity
    $('.cart-update-form input[name="quantity"]').on('change', function(e) {
        e.preventDefault();

        const form = $(this).closest('form');
        const url = form.attr('action');
        const quantity = $(this).val();

        $.ajax({
            url: url,
            type: 'POST',
            data: form.serialize(), // надсилаємо всі дані форми (включаючи csrf_token)
            success: function(response) {
                // ПЕРЕЗАВАНТАЖЕННЯ: Після успішного оновлення кошика
                if (response.status === 'ok') {
                    // console.log("Кількість оновлено");
                    window.location.reload();
                }
            },
            error: function(xhr, status, error) {
                console.error("Помилка оновлення кошика:", error);
            }
        });
    });


    // 2. НОВА ЛОГІКА: ВИДАЛЕННЯ ТОВАРУ (AJAX)
    // Припускаємо, що ваші кнопки видалення мають CSS-клас .js-cart-remove
    $('.js-cart-remove').on('click', function(e) {
        e.preventDefault();

        // Знаходимо форму, яка відповідає цій кнопці видалення
        const form = $(this).closest('form');
        const url = form.attr('action');

        // Оскільки видалення — це зазвичай POST-запит,
        // ми використовуємо form.serialize() для відправки CSRF-токена.
        $.ajax({
            url: url,
            type: 'POST',
            data: form.serialize(),
            success: function(response) {
                if (response.status === 'ok') {
                    // console.log("Товар видалено");
                    // Після успішного видалення оновлюємо сторінку
                    window.location.reload();
                }
            },
            error: function(xhr, status, error) {
                console.error("Помилка видалення товару:", error);
            }
        });
    });

});