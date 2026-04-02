document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('toggleFormBtn');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const formTitle = document.getElementById('formTitle');
    const productDescription = document.getElementById('productDescription');

    toggleBtn.addEventListener('click', () => {
        if (loginForm.classList.contains('hidden-form')) {
            // Переключаем на форму входа
            productDescription.style.display = 'none';
            registerForm.style.display = 'none';
            loginForm.classList.remove('hidden-form');
            toggleBtn.textContent = 'Назад к регистрации';
            formTitle.textContent = 'Вход в систему';
        } else {
            // Переключаем на форму регистрации
            productDescription.style.display = 'block';
            registerForm.style.display = 'block';
            loginForm.classList.add('hidden-form');
            toggleBtn.textContent = 'Вход';
            formTitle.textContent = 'Регистрация HR-менеджера';
        }
    });
});