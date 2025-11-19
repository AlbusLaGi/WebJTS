document.addEventListener('DOMContentLoaded', function() {
    const requiereOfrendaCheckbox = document.getElementById('id_requiere_ofrenda');
    const valorOfrendaField = document.querySelector('.field-valor_ofrenda');

    function toggleValorOfrendaField() {
        if (requiereOfrendaCheckbox.checked) {
            valorOfrendaField.style.display = 'block';
        } else {
            valorOfrendaField.style.display = 'none';
        }
    }

    // Ejecutar al cargar la página para establecer el estado inicial
    toggleValorOfrendaField();

    // Añadir event listener para cambios en el checkbox
    requiereOfrendaCheckbox.addEventListener('change', toggleValorOfrendaField);
});