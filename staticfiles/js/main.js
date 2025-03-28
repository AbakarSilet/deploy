// JavaScript de base
document.addEventListener('DOMContentLoaded', function () {
    console.log('Document chargé');

    // Faire disparaître les messages après 5 secondes
    setTimeout(function () {
        const messages = document.querySelectorAll('.messages div');
        messages.forEach(msg => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 500);
        });
    }, 5000);
});