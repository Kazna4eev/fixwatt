document.addEventListener('DOMContentLoaded', function () {
    const themeToggle = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement; // Отримуємо тег <html>

    // Функція для застосування теми
    function applyTheme(theme) {
        if (theme === 'dark') {
            htmlElement.setAttribute('data-bs-theme', 'dark');
        } else {
            htmlElement.setAttribute('data-bs-theme', 'light');
        }
    }

    // 1. При завантаженні сторінки застосовуємо збережену тему
    const savedTheme = localStorage.getItem('theme') || 'light';
    applyTheme(savedTheme);

    // 2. Додаємо обробник події для кнопки
    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            // Перевіряємо поточну тему і перемикаємо її
            const newTheme = htmlElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';

            // Застосовуємо нову тему
            applyTheme(newTheme);

            // Зберігаємо вибір користувача у localStorage
            localStorage.setItem('theme', newTheme);
        });
    }
});