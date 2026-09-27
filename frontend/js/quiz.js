const quizState = {
    questions: [],
    currentIndex: 0,
    selectedAnswers: {},
    loading: false,
};

const loadingEl = document.getElementById('quizLoading');
const startScreen = document.getElementById('quizStart');
const quizActive = document.getElementById('quizActive');
const quizResult = document.getElementById('quizResult');
const quizError = document.getElementById('quizError');
const quizErrorMessage = document.getElementById('quizErrorMessage');
const questionNumber = document.getElementById('questionNumber');
const questionCount = document.getElementById('questionCount');
const questionText = document.getElementById('questionText');
const quizOptions = document.getElementById('quizOptions');
const progressBar = document.getElementById('quizProgress');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const submitQuizBtn = document.getElementById('submitQuizBtn');
const retakeBtn = document.getElementById('retakeBtn');
const resultScore = document.getElementById('resultScore');
const resultPercentage = document.getElementById('resultPercentage');
const resultLevel = document.getElementById('resultLevel');
const resultMessage = document.getElementById('resultMessage');
const resultIcon = document.getElementById('resultIcon');
const reviewContent = document.getElementById('reviewContent');

const startQuizBtn = document.getElementById('startQuizBtn');

function showLoading(show) {
    if (loadingEl) {
        loadingEl.style.display = show ? 'block' : 'none';
    }
}

function showStartScreen() {
    if (startScreen) startScreen.style.display = 'block';
    if (quizActive) quizActive.style.display = 'none';
    if (quizResult) quizResult.classList.remove('show');
    if (quizError) quizError.style.display = 'none';
}

function showQuizScreen() {
    if (startScreen) startScreen.style.display = 'none';
    if (quizActive) quizActive.style.display = 'block';
    if (quizResult) quizResult.classList.remove('show');
    if (quizError) quizError.style.display = 'none';
}

function showResultScreen() {
    if (startScreen) startScreen.style.display = 'none';
    if (quizActive) quizActive.style.display = 'none';
    if (quizResult) quizResult.classList.add('show');
    if (quizError) quizError.style.display = 'none';
}

function showError(message) {
    if (quizErrorMessage) quizErrorMessage.textContent = message;
    if (quizError) quizError.style.display = 'block';
    if (loadingEl) loadingEl.style.display = 'none';
}

function escapeHtml(text) {
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function formatLevel(level) {
    if (level === 'good') return 'Good Privacy Awareness';
    if (level === 'moderate') return 'Moderate Awareness';
    return 'Needs Improvement';
}

function getResultMessage(level) {
    const messages = {
        good: 'Excellent work — you understand the essentials of digital privacy and online security.',
        moderate: 'You have a solid base of awareness. A few more safe habits can strengthen your protection.',
        needs_improvement: 'You are beginning your privacy journey. Review the learning resources and retake the quiz to improve.',
    };

    return messages[level] || messages.needs_improvement;
}

function renderQuestion() {
    const currentQuestion = quizState.questions[quizState.currentIndex];
    if (!currentQuestion) return;

    const total = quizState.questions.length;
    questionNumber.textContent = `Question ${quizState.currentIndex + 1}`;
    questionCount.textContent = `${quizState.currentIndex + 1} of ${total}`;
    questionText.textContent = currentQuestion.question;
    quizOptions.innerHTML = '';

    const selectedAnswer = quizState.selectedAnswers[currentQuestion.id];
    const optionLetters = ['A', 'B', 'C', 'D'];

    currentQuestion.options.forEach((option, index) => {
        const optionBtn = document.createElement('button');
        optionBtn.type = 'button';
        optionBtn.className = 'quiz-option';
        optionBtn.setAttribute('role', 'radio');
        optionBtn.setAttribute('aria-checked', selectedAnswer === index ? 'true' : 'false');
        if (selectedAnswer === index) {
            optionBtn.classList.add('selected');
        }

        optionBtn.innerHTML = `
            <span class="quiz-option-letter">${optionLetters[index]}</span>
            <span>${escapeHtml(option)}</span>
        `;

        optionBtn.addEventListener('click', () => {
            quizState.selectedAnswers[currentQuestion.id] = index;
            renderQuestion();
        });

        quizOptions.appendChild(optionBtn);
    });

    const progress = ((quizState.currentIndex + 1) / total) * 100;
    progressBar.style.width = `${progress}%`;

    prevBtn.disabled = quizState.currentIndex === 0;
    nextBtn.style.display = quizState.currentIndex === total - 1 ? 'none' : 'inline-flex';
    submitQuizBtn.style.display = quizState.currentIndex === total - 1 ? 'inline-flex' : 'none';
}

async function loadQuiz() {
    quizState.loading = true;
    showLoading(true);

    try {
        const response = await fetch('/api/quiz/');
        if (!response.ok) {
            throw new Error('Unable to load quiz questions.');
        }

        const data = await response.json();
        quizState.questions = data.questions || [];

        if (!quizState.questions.length) {
            throw new Error('No quiz questions were returned.');
        }

        showStartScreen();
    } catch (error) {
        showError(error.message || 'Please check your connection and try again.');
    } finally {
        quizState.loading = false;
        showLoading(false);
    }
}

function handleNext() {
    const total = quizState.questions.length;
    if (quizState.currentIndex < total - 1) {
        quizState.currentIndex += 1;
        renderQuestion();
    }
}

function handlePrevious() {
    if (quizState.currentIndex > 0) {
        quizState.currentIndex -= 1;
        renderQuestion();
    }
}

async function submitQuiz() {
    const payload = { answers: quizState.selectedAnswers };
    if (Object.keys(payload.answers).length !== quizState.questions.length) {
        alert('Please answer all questions before submitting the quiz.');
        return;
    }

    try {
        const response = await fetch('/api/quiz/result/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || 'The quiz could not be submitted.');
        }

        const result = await response.json();
        const level = result.awareness_level || 'needs_improvement';

        resultScore.textContent = `${result.score}/${result.total_questions}`;
        resultPercentage.textContent = `${result.percentage}%`;
        resultLevel.textContent = formatLevel(level);
        resultLevel.className = `result-level ${level}`;
        resultIcon.className = `result-icon ${level}`;
        resultIcon.innerHTML = level === 'good' ? '<i class="fas fa-trophy"></i>' : level === 'moderate' ? '<i class="fas fa-star"></i>' : '<i class="fas fa-exclamation-triangle"></i>';
        resultMessage.textContent = getResultMessage(level);

        reviewContent.innerHTML = '';
        (result.details || []).forEach((item) => {
            const row = document.createElement('div');
            row.className = 'review-question';
            const userAnswer = item.user_answer;
            const correctIndex = item.correct;
            const userText = item.options[userAnswer] || 'No answer selected';
            const correctText = item.options[correctIndex];

            row.innerHTML = `
                <div class="review-question-text">${escapeHtml(item.question)}</div>
                <div class="review-answer ${item.is_correct ? 'correct-answer' : 'wrong-answer'}">
                    <i class="${item.is_correct ? 'fas fa-check-circle' : 'fas fa-times-circle'}"></i>
                    <span>Your answer: ${escapeHtml(userText)}</span>
                </div>
                <div class="review-answer correct-answer">
                    <i class="fas fa-check-circle"></i>
                    <span>Correct answer: ${escapeHtml(correctText)}</span>
                </div>
            `;
            reviewContent.appendChild(row);
        });

        showResultScreen();
    } catch (error) {
        alert(error.message || 'Unable to submit quiz.');
    }
}

function resetQuiz() {
    quizState.currentIndex = 0;
    quizState.selectedAnswers = {};
    showStartScreen();
    progressBar.style.width = '0%';
    renderQuestion();
}

function getCSRFToken() {
    const cookie = document.cookie
        .split('; ')
        .find((part) => part.startsWith('csrftoken='));

    return cookie ? cookie.split('=')[1] : '';
}

if (startQuizBtn) {
    startQuizBtn.addEventListener('click', () => {
        showQuizScreen();
        renderQuestion();
    });
}

if (prevBtn) {
    prevBtn.addEventListener('click', handlePrevious);
}

if (nextBtn) {
    nextBtn.addEventListener('click', handleNext);
}

if (submitQuizBtn) {
    submitQuizBtn.addEventListener('click', submitQuiz);
}

if (retakeBtn) {
    retakeBtn.addEventListener('click', () => {
        resetQuiz();
    });
}

window.addEventListener('load', loadQuiz);
