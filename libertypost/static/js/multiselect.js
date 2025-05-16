document.addEventListener('DOMContentLoaded', function () {
    const multiselect = document.getElementById('multiselect');
    const selector = document.getElementById('multiselect-selector');
    const dropdown = document.getElementById('multiselect-dropdown');
    const arrow = selector.querySelector('.multiselect-arrow');
    const originalSelect = document.getElementById('cats');

    let selectedOptions = [];

    function init() {
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

            optionElement.addEventListener('click', function (e) {
                e.stopPropagation();
                toggleOption(option.value, option.textContent);
            });
        });

        selector.addEventListener('click', function () {
            toggleDropdown();
        });

        document.addEventListener('click', function (e) {
            if (!multiselect.contains(e.target)) {
                closeDropdown();
            }
        });

        dropdown.addEventListener('click', function (e) {
            e.stopPropagation();
        });
    }

    function toggleDropdown() {
        dropdown.classList.toggle('open');
        arrow.classList.toggle('open');
    }

    function closeDropdown() {
        dropdown.classList.remove('open');
        arrow.classList.remove('open');
    }

    function toggleOption(value, text) {
        const index = selectedOptions.findIndex((opt) => opt.value === value);
        const optionElement = dropdown.querySelector(
            `.multiselect-option[data-value="${value}"]`
        );
        const checkbox = optionElement.querySelector('.multiselect-checkbox');

        if (index !== -1) {
            selectedOptions.splice(index, 1);
            optionElement.classList.remove('selected');
            checkbox.classList.remove('checked');

            for (let i = 0; i < originalSelect.options.length; i++) {
                if (originalSelect.options[i].value === value) {
                    originalSelect.options[i].selected = false;
                    break;
                }
            }
        } else {
            selectedOptions.push({ value, text });
            optionElement.classList.add('selected');
            checkbox.classList.add('checked');

            for (let i = 0; i < originalSelect.options.length; i++) {
                if (originalSelect.options[i].value === value) {
                    originalSelect.options[i].selected = true;
                    break;
                }
            }
        }

        updateSelectedDisplay();
    }

    function updateSelectedDisplay() {
        while (selector.firstChild) {
            if (selector.firstChild === arrow) {
                break;
            }
            selector.removeChild(selector.firstChild);
        }

        if (selectedOptions.length === 0) {
            const placeholder = document.createElement('span');
            placeholder.className = 'multiselect-placeholder';
            placeholder.textContent = 'Не выбрано';
            selector.insertBefore(placeholder, arrow);
        } else {
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

        updateOriginalSelect();
    }

    function updateOriginalSelect() {
        for (let i = 0; i < originalSelect.options.length; i++) {
            originalSelect.options[i].selected = false;
        }

        selectedOptions.forEach((option) => {
            for (let i = 0; i < originalSelect.options.length; i++) {
                if (originalSelect.options[i].value === option.value) {
                    originalSelect.options[i].selected = true;
                    break;
                }
            }
        });
    }

    init();
});
