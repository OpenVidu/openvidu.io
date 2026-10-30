document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".copy-inline").forEach((el) => {
        const btn = el.querySelector(".copy-btn");

        // Add pointer cursor to make it look clickable
        btn.style.cursor = 'pointer';

        btn.addEventListener("click", () => {
            const text = el.getAttribute("data-copy");
            const originalTitle = btn.getAttribute("title");
            const originalHTML = btn.innerHTML;

            navigator.clipboard.writeText(text).then(() => {
                // Change color to blue to indicate success
                btn.style.color = '#2196F3';
                btn.style.transition = 'color 0.3s ease';
                btn.setAttribute("title", "Copied");

                // Revert after 1000ms
                setTimeout(() => {
                    btn.style.color = '';
                    btn.setAttribute("title", originalTitle);
                }, 100);
            }).catch(() => {
                // Change color to red if copy failed
                btn.style.color = '#f44336';
                btn.style.transition = 'color 0.3s ease';
                btn.innerHTML = ':material-close:';
                btn.setAttribute("title", "Failed to copy");

                // Revert after 1000ms
                setTimeout(() => {
                    btn.style.color = '';
                    btn.innerHTML = originalHTML;
                    btn.setAttribute("title", originalTitle);
                }, 100);
            });
        });
    });
});