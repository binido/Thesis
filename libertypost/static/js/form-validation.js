document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form')
    const inputs = form.querySelectorAll('input[required]')
    const submitButton = form.querySelector('input[type="submit"]')

    const checkFormValidity = () => {
        const isFormValid = Array.from(inputs).every(input => input.value.trim() !== '')
        submitButton.disabled = !isFormValid
    }

    inputs.forEach(input => {
        input.addEventListener('input', checkFormValidity)
    })

    checkFormValidity()
}) 