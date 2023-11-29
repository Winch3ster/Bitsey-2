document.addEventListener('DOMContentLoaded', function () {
    var checkboxes = document.querySelectorAll('.form-check-input');

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            // Build a list of selected values
            var selectedValues = Array.from(checkboxes)
                .filter(checkbox => checkbox.checked)
                .map(checkbox => checkbox.value);

            // Send an API request with selected values
            // You can use Fetch API or any other AJAX library for this
            // Example using Fetch API:
            fetch('/api/search/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ platforms: selectedValues }),
            })
            .then(response => response.json())
            .then(data => {
                // Handle the response data
                console.log(data);
            })
            .catch(error => console.error('Error:', error));
        });
    });
});