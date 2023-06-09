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
                window.location.href = '/';
                throw new Error('Error checking token');
            }
        } catch (error) {
            console.error('Error checking token:', error);
        }
    }
}



async function setUserInfos() {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch('/home/me', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (response.ok) {
            const userData = await response.json();
            const userNameElement = document.getElementById('user-infos');
            userNameElement.innerHTML = `<span id="user-name-text" style="color: white; padding-right: 10px;">${userData.username}</span>`;
            // Replace the balance value below with the correct balance from userData
            userNameElement.innerHTML += `<span id="user-balance" class="badge bg-primary rounded-pill px-3 py-2">Balance: ${userData.balance.toFixed(2)} Coin</span>`;
        } else {
            window.location.href = '/';
            console.error('Failed to fetch user information');
        }
    } catch (error) {
        console.error('Error fetching user information:', error);
    }
}

window.onload = async () => {
    await checkTokenAndRedirect();
    await setUserInfos();
};
