document.addEventListener("DOMContentLoaded", function () {
    // Back to Top Button
    const backToTopBtn = document.getElementById('backToTop');
    window.addEventListener('scroll', () => {
        if(window.scrollY > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({top: 0, behavior: 'smooth'});
    });

    // Newsletter Modal Popup (show after 10 seconds)
    const newsletterModal = new bootstrap.Modal(document.getElementById('newsletterModal'));
    setTimeout(() => {
        newsletterModal.show();
    }, 10000);

    function closeModal() {
        newsletterModal.hide();
    }

    // Newsletter AJAX handler
    function handleNewsletterForm(formId) {
        const form = document.getElementById(formId);
        if (!form) return;

        form.addEventListener("submit", function (e) {
            e.preventDefault();

            const email = form.querySelector("input[name='email']").value;
            const submitBtn = form.querySelector("button[type='submit']");
            const csrfTokenInput = form.querySelector("input[name='csrfmiddlewaretoken']");
            const csrfToken = csrfTokenInput ? csrfTokenInput.value : "";

            if (submitBtn) submitBtn.disabled = true;

            fetch("/subscribe/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ email: email })
            })
            .then(res => res.json())
            .then(data => {
                alert(data.message);

                if (data.success) {
                    form.reset();
                    if (formId === "popupNewsletterForm") {
                        const modalEl = document.getElementById("newsletterModal");
                        const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
                        if (modal) {
                            modal.hide();
                        }
                    }
                }
            })
            .catch(err => {
                console.error("Newsletter error:", err);
                alert("Something went wrong. Please try again.");
            })
            .finally(() => {
                if (submitBtn) submitBtn.disabled = false;
            });
        });
    }

    handleNewsletterForm("popupNewsletterForm");
    handleNewsletterForm("sidebarNewsletterForm");
});
