document.getElementById('contactUs').addEventListener('click', () => {
    window.location.href = '/home/aboutUs';
});


document.getElementById('order-private').addEventListener('click', () => {
    window.location.href = '/home/checkout?planId=private';
});

document.getElementById('order-professional').addEventListener('click', () => {
    window.location.href = '/home/checkout?planId=professional';
});
