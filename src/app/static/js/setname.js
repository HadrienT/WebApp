async function setName() {
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
            const userNameElement = document.getElementById('user-name');
            userNameElement.innerText = userData.username;
        } else {
            window.location.href = '/';
            console.error('Failed to fetch user information');
        }
    } catch (error) {
        console.error('Error fetching user information:', error);
    }
}

window.onload = async () => {
    await setName();
};