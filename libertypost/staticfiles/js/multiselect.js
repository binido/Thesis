document.addEventListener('DOMContentLoaded', function () {
    const multiselect = document.getElementById('multiselect');
    const selector = document.getElementById('multiselect-selector');
    const dropdown = document.getElementById('multiselect-dropdown');
    const arrow = selector.querySelector('.multiselect-arrow');
    const originalSelect = document.getElementById('cats');

    // Массив для хранения выбранных опций
    let selectedOptions = [];

    // Функция инициализации
    function init() {
        // Создаем опции в выпадающем списке на основе исходного select
        const options = Array.from(originalSelect.options);
        options.forEach((option) => {
            const optionElement = document.createElement('div');
            optionElement.className = 'multiselect-option';
            optionElement.dataset.value = option.value;

            const checkbox = document.createElement('div');
            checkbox.className = 'multiselect-checkbox';

            const label = document.createElement('span');
            label.textContent = option.textContent;

            optionElement.appendChild(checkbox);
            optionElement.appendChild(label);
            dropdown.appendChild(optionElement);

            // Добавляем обработчик клика по опции
            optionElement.addEventListener('click', function (e) {
                e.stopPropagation();
                toggleOption(option.value, option.textContent);
            });
        });

        // Обработчик клика по селектору
        selector.addEventListener('click', function () {
            toggleDropdown();
        });

        // Закрытие выпадающего списка при клике вне его области
        document.addEventListener('click', function (e) {
            if (!multiselect.contains(e.target)) {
                closeDropdown();
            }
        });

        // Предотвращаем закрытие выпадающего списка при клике внутри него
        dropdown.addEventListener('click', function (e) {
            e.stopPropagation();
        });
    }

    // Функция для открытия/закрытия выпадающего списка
    function toggleDropdown() {
        dropdown.classList.toggle('open');
        arrow.classList.toggle('open');
    }

    // Функция для закрытия выпадающего списка
    function closeDropdown() {
        dropdown.classList.remove('open');
        arrow.classList.remove('open');
    }

    // Функция для выбора/отмены выбора опции
    function toggleOption(value, text) {
        const index = selectedOptions.findIndex((opt) => opt.value === value);
        const optionElement = dropdown.querySelector(
            `.multiselect-option[data-value="${value}"]`
        );
        const checkbox = optionElement.querySelector('.multiselect-checkbox');

        if (index !== -1) {
            // Отменяем выбор опции
            selectedOptions.splice(index, 1);
            optionElement.classList.remove('selected');
            checkbox.classList.remove('checked');

            // Снимаем выбор в исходном select
            for (let i = 0; i < originalSelect.options.length; i++) {
                if (originalSelect.options[i].value === value) {
                    originalSelect.options[i].selected = false;
                    break;
                }
            }
        } else {
            // Выбираем опцию
            selectedOptions.push({ value, text });
            optionElement.classList.add('selected');
            checkbox.classList.add('checked');

            // Выбираем в исходном select
            for (let i = 0; i < originalSelect.options.length; i++) {
                if (originalSelect.options[i].value === value) {
                    originalSelect.options[i].selected = true;
                    break;
                }
            }
        }

        updateSelectedDisplay();
    }

    // Функция для обновления отображения выбранных опций
    function updateSelectedDisplay() {
        // Очищаем содержимое селектора
        while (selector.firstChild) {
            if (selector.firstChild === arrow) {
                break;
            }
            selector.removeChild(selector.firstChild);
        }

        if (selectedOptions.length === 0) {
            // Если ничего не выбрано, показываем плейсхолдер
            const placeholder = document.createElement('span');
            placeholder.className = 'multiselect-placeholder';
            placeholder.textContent = 'Не выбрано';
            selector.insertBefore(placeholder, arrow);
        } else {
            // Показываем выбранные опции
            selectedOptions.forEach((option) => {
                const tag = document.createElement('div');
                tag.className = 'multiselect-tag';

                const tagText = document.createElement('span');
                tagText.textContent = option.text;

                const tagClose = document.createElement('span');
                tagClose.className = 'multiselect-tag-close';
                tagClose.textContent = '×';
                tagClose.addEventListener('click', function (e) {
                    e.stopPropagation();
                    toggleOption(option.value, option.text);
                });

                tag.appendChild(tagText);
                tag.appendChild(tagClose);
                selector.insertBefore(tag, arrow);
            });
        }

        // Обновляем исходный select для отправки формы
        updateOriginalSelect();
    }

    // Функция для синхронизации с исходным select
    function updateOriginalSelect() {
        // Сначала снимаем все выделения
        for (let i = 0; i < originalSelect.options.length; i++) {
            originalSelect.options[i].selected = false;
        }

        // Затем выбираем нужные опции
        selectedOptions.forEach((option) => {
            for (let i = 0; i < originalSelect.options.length; i++) {
                if (originalSelect.options[i].value === option.value) {
                    originalSelect.options[i].selected = true;
                    break;
                }
            }
        });
    }

    // Инициализируем компонент
    init();
});
