async function checkTokenAndRedirect() {
    const token = localStorage.getItem('token');

    if (token) {
        try {
            const response = await fetch('/auth/token', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + token,
                },
            });

            if (!response.ok) {
                console.log('Token is not valid');
                localStorage.removeItem('token');
                document.cookie = 'cookie_token' + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                throw new Error('Error checking token');
            }
            else {
                console.log('Token is valid');
                // Token is valid, load the content and replace the current page
                try {
                    const responseBis = await fetch('/home', {
                        method: 'GET',
                        headers: {
                            'Authorization': 'Bearer ' + token,
                        },
                    });
                    if (!responseBis.ok) {
                        throw new Error('Error loading home page');
                    }
                    const homeData = await response.text();
                    document.open();
                    document.write(homeData);
                    document.close();
                    window.history.replaceState({}, 'Home page', '/home');
                } catch (error) {
                    console.error('Error loading home page:', error);
                }
            }
        } catch (error) {
            console.error('Error checking token:', error);
        }
    }
}

window.addEventListener('DOMContentLoaded', () => {
    console.log('Window loaded');
    checkTokenAndRedirect();
});