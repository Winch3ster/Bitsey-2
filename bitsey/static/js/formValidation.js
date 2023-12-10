function validateForm() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    if (username === '' || password === '') {
        alert('Please fill out all fields');
        return false;
    }

    // Additional validation logic can be added here

    // If validation passes, submit the form
    document.getElementById('myForm').submit();
}