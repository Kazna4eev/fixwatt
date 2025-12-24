$(function() {

    // Отримуємо URL-адреси з HTML-елементів (data-url)
    const citySearchUrl = $('#city-search-url').data('url');
    const warehouseSearchUrl = $('#warehouse-search-url').data('url');

    if (!citySearchUrl || !warehouseSearchUrl) {
        console.error("Помилка: Не знайдено URL-адреси Нової Пошти у шаблоні HTML.");
        // Можна відключити поля для запобігання помилок
        $("#id_city_name").prop('disabled', true);
        $("#id_warehouse_name").prop('disabled', true);
        return;
    }

    // --- 1. АВТОЗАПОВНЕННЯ МІСТ ---
    $("#id_city_name").autocomplete({
        source: function(request, response) {

            $.ajax({
                url: citySearchUrl, // Використовуємо коректний URL
                dataType: "json",
                data: {
                    term: request.term
                },
                success: function(data) {
                    const cities = data.cities.map(item => ({
                        label: item.description,
                        value: item.description,
                        ref: item.ref
                    }));
                    response(cities);
                },
                error: function() {
                    console.error("Помилка: API Нової Пошти для міст недоступний.");
                    response([]);
                }
            });
        },
        minLength: 2,

        select: function(event, ui) {
            const cityRef = ui.item.ref;
            const cityName = ui.item.label;

            $("#id_city_ref").val(cityRef);
            $("#id_city_name").val(cityName);

            $("#id_warehouse_ref").val('');
            $("#id_warehouse_name").val('');
            $("#id_warehouse_name").prop('disabled', false);

            $("#id_warehouse_name").focus().autocomplete("search");

            event.preventDefault();
        }
    }).focus(function(){
        $(this).autocomplete("search");
    });


    // --- 2. АВТОЗАПОВНЕННЯ ВІДДІЛЕНЬ ---
    $("#id_warehouse_name").autocomplete({
        source: function(request, response) {
            const cityRef = $("#id_city_ref").val();

            if (!cityRef) {
                return;
            }

            $.ajax({
                url: warehouseSearchUrl, // Використовуємо коректний URL
                dataType: "json",
                data: {
                    city_ref: cityRef,
                    term: request.term
                },
                success: function(data) {
                    const warehouses = data.warehouses.map(item => ({
                        label: item.description,
                        value: item.description,
                        ref: item.ref
                    }));
                    response(warehouses);
                },
                error: function() {
                    console.error("Помилка: API Нової Пошти для відділень недоступний.");
                    response([]);
                }
            });
        },
        minLength: 1,

        select: function(event, ui) {
            $("#id_warehouse_ref").val(ui.item.ref);
            $("#id_warehouse_name").val(ui.item.label);

            event.preventDefault();
        }
    }).focus(function(){
        $(this).autocomplete("search");
    });
});