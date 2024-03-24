// Получаем все элементы с классом deleteButton
const deleteButtons = document.querySelectorAll(".delete-button");
const restoreButtons = document.querySelectorAll(".restore-button");

// Перебираем полученные элементы и назначаем обработчик события click каждому из них
deleteButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        if (confirm("Вы уверены, что хотите удалить рецепт?")) {
            const recipeId = this.getAttribute("data-recipe-id");
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Получаем CSRF токен из метатега
            const xhr = new XMLHttpRequest();
            const cardElement = this.closest('.card');
            const linkElement = this.closest('.delete-button');
            xhr.open("POST", "/book/recipe/delete/" + recipeId + "/", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.setRequestHeader("X-CSRFToken", csrfToken); // Устанавливаем CSRF токен в заголовке запроса
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    if (xhr.status === 200) {
                        alert("Рецепт успешно удален!");
                        cardElement.classList.remove('text-body');
                        cardElement.classList.add('text-body-secondary');

                        linkElement.classList.add('d-none');
                    } else {
                        alert("Ошибка при удалении рецепта");

                    }
                }
            };
            xhr.send(JSON.stringify({recipe_id: recipeId}));
        }
    });
});

restoreButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        const recipeId = this.getAttribute("data-recipe-id");
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // Получаем CSRF токен из метатега
        const xhr = new XMLHttpRequest();
        const cardElement = this.closest('.card');
        const linkElement = this.closest('.restore-button');
        xhr.open("POST", "/book/recipe/restore/" + recipeId + "/", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("X-CSRFToken", csrfToken); // Устанавливаем CSRF токен в заголовке запроса
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    alert("Рецепт успешно восстановлен!");
                    cardElement.classList.remove('text-body-secondary');
                    cardElement.classList.add('text-body');

                    linkElement.classList.add('d-none');
                } else {
                    alert("Ошибка при восстановлении рецепта");
                }
            }
        };
        xhr.send();
    });
})