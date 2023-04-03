function logout() {
    localStorage.removeItem('token');
    document.cookie = 'cookie_token' + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/';
}