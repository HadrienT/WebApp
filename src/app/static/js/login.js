document.getElementById('register').addEventListener('click', () => {
    window.location.href = '/user/register';
});

document.getElementById('signin-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('floatingInput').value;
    const password = document.getElementById('floatingPassword').value;
    const rememberMe = document.querySelector('input[type="checkbox"]').checked;

    const formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);

    try {
        const response = await fetch('/auth/token', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            },
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.access_token); // Save token to local storage
            document.cookie = `cookie_token=${data.access_token}; path=/; max-age=${30 * 60 * 60}`;

            // Make a GET request to the /home endpoint with the token
            const homeResponse = await fetch('/home', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + data.access_token,
                },
            });

            if (homeResponse.ok) {
                const homeData = await homeResponse.text();
                document.open();
                document.write(homeData);
                document.close();
                window.history.pushState({}, 'Home page', '/home');

            } else {
                alert('Failed to load home page');
            }
        } else {
            // Handle errors
            alert('Sign in failed');
        }
    } catch (error) {
        console.error(error);
    }
});