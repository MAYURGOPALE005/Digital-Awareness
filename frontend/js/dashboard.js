document.addEventListener('DOMContentLoaded', async () => {
    const totalParticipantsEl = document.getElementById('totalParticipants');
    const averageScoreEl = document.getElementById('averageScore');
    const goodPercentageEl = document.getElementById('goodPercentage');
    const moderatePercentageEl = document.getElementById('moderatePercentage');
    const needsPercentageEl = document.getElementById('needsPercentage');
    const awarenessChart = document.getElementById('awarenessChart');
    const quizChart = document.getElementById('quizChart');

    async function loadDashboardData() {
        try {
            const [surveyResultsResponse, quizStatsResponse] = await Promise.all([
                fetch('/api/survey/results/'),
                fetch('/api/quiz/statistics/'),
            ]);

            if (!surveyResultsResponse.ok || !quizStatsResponse.ok) {
                throw new Error('Dashboard data could not be loaded.');
            }

            const surveyResults = await surveyResultsResponse.json();
            const quizStats = await quizStatsResponse.json();

            totalParticipantsEl.textContent = surveyResults.total_responses || 0;
            averageScoreEl.textContent = quizStats.average_score ? Number(quizStats.average_score).toFixed(1) : '0.0';
            goodPercentageEl.textContent = `${quizStats.good_percentage || 0}%`;
            moderatePercentageEl.textContent = `${quizStats.moderate_percentage || 0}%`;
            needsPercentageEl.textContent = `${quizStats.needs_improvement_percentage || 0}%`;

            renderAwarenessChart(surveyResults);
            renderQuizChart(quizStats);
        } catch (error) {
            awarenessChart.innerHTML = '<div class="empty-state">Unable to load awareness data.</div>';
            quizChart.innerHTML = '<div class="empty-state">Unable to load quiz statistics.</div>';
        }
    }

    function renderAwarenessChart(results) {
        const before = Number(results.privacy_awareness_distribution?.not_aware || 0) + Number(results.privacy_awareness_distribution?.slightly_aware || 0);
        const after = Number(results.privacy_awareness_distribution?.moderately_aware || 0) + Number(results.privacy_awareness_distribution?.very_aware || 0);

        const values = [
            { label: 'Before Awareness', value: before },
            { label: 'After Awareness', value: after },
        ];

        const max = Math.max(...values.map((item) => item.value), 1);

        awarenessChart.innerHTML = values.map((item) => `
            <div class="bar-row">
                <div class="bar-label">${item.label}</div>
                <div class="bar-track"><div class="bar-fill" style="width: ${(item.value / max) * 100}%"></div></div>
                <div class="bar-value">${item.value}</div>
            </div>
        `).join('');
    }

    function renderQuizChart(stats) {
        const entries = [
            { label: 'Good', value: Number(stats.good_percentage || 0) },
            { label: 'Moderate', value: Number(stats.moderate_percentage || 0) },
            { label: 'Needs Improvement', value: Number(stats.needs_improvement_percentage || 0) },
        ];

        const max = Math.max(...entries.map((item) => item.value), 1);

        quizChart.innerHTML = entries.map((item) => `
            <div class="bar-row">
                <div class="bar-label">${item.label}</div>
                <div class="bar-track"><div class="bar-fill" style="width: ${(item.value / max) * 100}%"></div></div>
                <div class="bar-value">${item.value}%</div>
            </div>
        `).join('');
    }

    await loadDashboardData();
});
