
document.getElementById('cancel-btn').addEventListener('click', () => {
    window.location.href = '/'; // Navigate to the homepage
});

document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/user/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
    });

    if (response.ok) {
        const data = await response.json(); // Parse the JSON response
        localStorage.setItem('token', data.access_token); // Save token to local storage
        document.cookie = `cookie_token=${data.access_token}; path=/; max-age=${30 * 60 * 60}`;
        try {
            const response = await fetch('/home', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + localStorage.getItem('token'),
                },
            });

            if (response.ok) {
                // Token is valid, load the content and replace the current page
                const homeData = await response.text();
                document.open();
                document.write(homeData);
                document.close();
                window.history.pushState({}, 'Home page', '/home');
            } else {

                console.log('Token is not valid');
                localStorage.removeItem('token');
            }
        } catch (error) {
            console.error('Error checking token:', error);
        }
    } else {
        const data = await response.json(); // Parse the JSON response
        const errorMessage = data.detail || 'Error creating account. Please try again.';
        alert(errorMessage);
    }
});
