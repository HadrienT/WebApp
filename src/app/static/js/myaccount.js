async function checkTokenAndRedirect() {
    const token = localStorage.getItem('token');

    if (token) {
        try {
            const response = await fetch('/home/myaccount', {
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + token,
                },
            });

            if (response.ok) {
                // Token is valid, load the content and replace the current page
                const homeData = await response.text();
                document.open();
                document.write(homeData);
                document.close();
            } else {
                console.log('Token is not valid');
                localStorage.removeItem('token');
            }
        } catch (error) {
            console.error('Error checking token:', error);
        }
    }
}
document.getElementById('myaccount').addEventListener('click', async () => {
    await checkTokenAndRedirect();
});