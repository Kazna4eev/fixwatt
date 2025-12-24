$(function() {
    function initializeCartModalLogic() {
        $('form[action*="cart/add"]').on('submit', function(e) {
            e.preventDefault();

            // ЗБЕРІГАЄМО ЗМІННІ ФОРМИ
            const form = $(this);
            const url = form.attr('action');
            const data = form.serialize();

            // Виконуємо AJAX-запит
            $.ajax({
                type: 'POST',
                url: url,
                data: data,
                dataType: 'json',

                success: function(data) {
                    // === ТУТ ТИМЧАСОВЕ ПРИМУСОВЕ ПЕРЕНАПРАВЛЕННЯ ===
                    // Це змусить браузер негайно перейти, оновити сесію і відобразити кошик
                    if (data.status === 'ok') {
                        // Оновлюємо лічильник кошика (якщо він є)
                        if (data.quantity !== undefined) {
                            // Припустимо, що у вас є елемент з id="cart-total-quantity"
                            $('#cart-total-quantity').text(data.quantity);
                        }

                        // ПРИМУСОВЕ ПЕРЕНАПРАВЛЕННЯ:
                        window.location.href = CART_DETAIL_URL;
                    } else {
                        // Якщо Django повернув статус не 'ok', показуємо помилку
                        alert('Помилка додавання до кошика: невірний статус.');
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Помилка додавання до кошика:", error);
                    alert("Помилка додавання до кошика. Спробуйте пізніше.");
                }
            });
        });

        // Блок для кнопки 'goToCartButton' тепер не потрібен, оскільки ми перенаправляємо одразу.
        // Але ми його залишаємо, якщо ви вирішите повернути модальне вікно пізніше:
        // $('#goToCartButton').on('click', function() { /* ... */ });
    }

    setTimeout(initializeCartModalLogic, 50);
});