$(document).ready(function () {
    console.log("Product detail script loaded");
    // alert("JS Loaded! v2"); // Debug alert

    // Використовуємо делегування подій для надійності
    // Це працюватиме навіть якщо форма завантажується динамічно або DOM ще змінюється
    $(document).on('submit', '.add-to-cart-form', function (e) {
        console.log("Form submission intercepted");
        e.preventDefault();

        const form = $(this);
        const url = form.attr('action');
        const data = form.serialize();

        $.ajax({
            type: 'POST',
            url: url,
            data: data,
            dataType: 'json',
            success: function (data) {
                console.log("AJAX success", data);
                if (data.status === 'ok') {
                    // 1. Оновлюємо лічильник кошика
                    if (data.quantity !== undefined) {
                        var badge = $('#cart-badge');
                        badge.text(data.quantity);
                        badge.show();
                    }

                    // 2. Показуємо модальне вікно
                    var myModal = new bootstrap.Modal(document.getElementById('cartSuccessModal'));
                    myModal.show();
                } else {
                    alert('Сталася помилка. Спробуйте ще раз.');
                }
            },
            error: function (xhr, status, error) {
                console.error("AJAX error:", error);
                alert("Не вдалося додати товар. Перевірте з'єднання.");
            }
        });
    });

    // Кнопка "Перейти до кошика" в модальному вікні
    $('#goToCartButton').on('click', function () {
        window.location.href = CART_DETAIL_URL;
    });
});