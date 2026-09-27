document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('surveyForm');
    const status = document.getElementById('surveyStatus');

    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const payload = Object.fromEntries(formData.entries());

        if (!payload.age_group || !payload.internet_usage || !payload.platforms || !payload.privacy_awareness || !payload.password_practice || !payload.two_factor_auth || !payload.phishing_awareness || !payload.app_permissions || !payload.social_media_privacy || !payload.online_payment_safety) {
            status.innerHTML = '<div class="alert alert-error show"><p><strong>Please complete all required fields before submitting.</strong></p></div>';
            return;
        }

        status.innerHTML = '<div class="alert alert-info show"><p>Submitting survey...</p></div>';

        try {
            const response = await fetch('/api/survey/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify(payload),
            });

            const result = await response.json();

            if (!response.ok) {
                const errors = result.errors ? Object.entries(result.errors).map(([key, value]) => `${key}: ${value.join(', ')}`).join('<br>') : 'Please check the form and try again.';
                status.innerHTML = `<div class="alert alert-error show"><p><strong>Submission failed.</strong></p><p>${errors}</p></div>`;
                return;
            }

            form.reset();
            const successMessage = result.message || 'Survey submitted successfully! Your response has been recorded.';
            status.innerHTML = `<div class="alert alert-success show"><p><strong>Survey submitted successfully!</strong></p><p>${successMessage}</p></div>`;
            status.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } catch (error) {
            status.innerHTML = `<div class="alert alert-error show"><p><strong>Network error.</strong></p><p>Please try again later.</p></div>`;
        }
    });

    function getCSRFToken() {
        const cookie = document.cookie
            .split('; ')
            .find((part) => part.startsWith('csrftoken='));

        return cookie ? cookie.split('=')[1] : '';
    }
});
