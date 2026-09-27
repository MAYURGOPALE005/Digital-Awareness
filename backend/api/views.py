"""
DRF Views for the Digital Privacy Awareness CEP project.
Provides API endpoints for survey submission/results and quiz questions/results/statistics.
"""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Avg

from .models import SurveyResponse, QuizResult
from .serializers import SurveyResponseSerializer, QuizResultSerializer


# ---------------------------------------------------------------------------
# Quiz Questions — stored as a simple Python data structure (viva-friendly)
# ---------------------------------------------------------------------------

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "What is digital privacy?",
        "options": [
            "Keeping your computer clean from dust",
            "The ability to control what personal information you share online",
            "Having a fast internet connection",
            "Using social media every day"
        ],
        "correct": 1,
    },
    {
        "id": 2,
        "question": "Someone calls you and asks for your OTP (One-Time Password). What should you do?",
        "options": [
            "Share it immediately — they might be from your bank",
            "Share it only if they sound professional",
            "Never share your OTP with anyone — no legitimate organization will ask for it",
            "Post it on social media so you don't forget"
        ],
        "correct": 2,
    },
    {
        "id": 3,
        "question": "What is phishing?",
        "options": [
            "A type of outdoor sport",
            "A trick where attackers send fake messages or emails to steal your information",
            "A way to speed up your internet",
            "A privacy setting on social media"
        ],
        "correct": 1,
    },
    {
        "id": 4,
        "question": "What is Two-Factor Authentication (2FA)?",
        "options": [
            "Using two different phones",
            "Logging in with your username only",
            "An extra layer of security that requires a second verification step after your password",
            "Having two social media accounts"
        ],
        "correct": 2,
    },
    {
        "id": 5,
        "question": "Is it safe to use the same password for all your online accounts?",
        "options": [
            "Yes, it is easier to remember",
            "Yes, as long as it is a strong password",
            "No, if one account is hacked, all your accounts could be at risk",
            "It doesn't matter"
        ],
        "correct": 2,
    },
    {
        "id": 6,
        "question": "Why should you review app permissions on your phone?",
        "options": [
            "To make your phone look organized",
            "Because some apps request access to your camera, microphone, or location without needing it",
            "It is not necessary to review permissions",
            "To increase your phone's storage"
        ],
        "correct": 1,
    },
    {
        "id": 7,
        "question": "You receive a message with a link saying 'You have won ₹10,00,000! Click here to claim.' What should you do?",
        "options": [
            "Click the link immediately to claim the prize",
            "Forward it to all your friends",
            "Ignore and delete it — it is likely a scam",
            "Reply with your bank details"
        ],
        "correct": 2,
    },
    {
        "id": 8,
        "question": "Is public Wi-Fi safe for banking or entering passwords?",
        "options": [
            "Yes, public Wi-Fi is always secure",
            "Yes, if the cafe looks trustworthy",
            "No, public Wi-Fi can be insecure and attackers may intercept your data",
            "Only if you use it for less than 5 minutes"
        ],
        "correct": 2,
    },
    {
        "id": 9,
        "question": "Which of the following should you NOT share publicly online?",
        "options": [
            "Your favourite movie",
            "Your home address, phone number, or Aadhaar number",
            "A photo of your pet",
            "Your opinion on a book"
        ],
        "correct": 1,
    },
    {
        "id": 10,
        "question": "Why are privacy settings on social media important?",
        "options": [
            "They make your profile look better",
            "They help you get more followers",
            "They let you control who can see your posts, photos, and personal information",
            "They are not important at all"
        ],
        "correct": 2,
    },
]


# ---------------------------------------------------------------------------
# Survey Endpoints
# ---------------------------------------------------------------------------

@api_view(['POST'])
def survey_submit(request):
    """
    POST /api/survey/
    Submit a new community awareness survey response.
    """
    serializer = SurveyResponseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Survey submitted successfully! Your response has been recorded.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {"message": "Validation failed.", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['GET'])
def survey_results(request):
    """
    GET /api/survey/results/
    Returns aggregated survey statistics. No personally identifiable info exposed.
    """
    total = SurveyResponse.objects.count()

    if total == 0:
        return Response({
            "total_responses": 0,
            "age_distribution": {},
            "internet_usage_distribution": {},
            "privacy_awareness_distribution": {},
            "password_practice_distribution": {},
            "two_factor_auth_distribution": {},
            "phishing_awareness_distribution": {},
            "app_permissions_distribution": {},
            "social_media_privacy_distribution": {},
            "online_payment_safety_distribution": {},
        })

    def distribution(field):
        qs = (
            SurveyResponse.objects
            .values(field)
            .annotate(count=Count('id'))
            .order_by(field)
        )
        return {item[field]: item['count'] for item in qs}

    return Response({
        "total_responses": total,
        "age_distribution": distribution('age_group'),
        "internet_usage_distribution": distribution('internet_usage'),
        "privacy_awareness_distribution": distribution('privacy_awareness'),
        "password_practice_distribution": distribution('password_practice'),
        "two_factor_auth_distribution": distribution('two_factor_auth'),
        "phishing_awareness_distribution": distribution('phishing_awareness'),
        "app_permissions_distribution": distribution('app_permissions'),
        "social_media_privacy_distribution": distribution('social_media_privacy'),
        "online_payment_safety_distribution": distribution('online_payment_safety'),
    })


# ---------------------------------------------------------------------------
# Quiz Endpoints
# ---------------------------------------------------------------------------

@api_view(['GET'])
def quiz_questions(request):
    """
    GET /api/quiz/
    Returns all quiz questions with options (correct answers NOT included).
    """
    # Strip out the 'correct' key so the client cannot see answers
    questions_safe = []
    for q in QUIZ_QUESTIONS:
        questions_safe.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
        })
    return Response({"questions": questions_safe})


@api_view(['POST'])
def quiz_result(request):
    """
    POST /api/quiz/result/
    Receives the user's answers, calculates the score, saves the result,
    and returns score + correct answers.
    """
    answers = request.data.get('answers', {})

    if not answers:
        return Response(
            {"message": "No answers provided."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Calculate score
    score = 0
    results_detail = []
    for q in QUIZ_QUESTIONS:
        q_id = str(q["id"])
        user_answer = answers.get(q_id)
        is_correct = user_answer == q["correct"]
        if is_correct:
            score += 1
        results_detail.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
            "correct": q["correct"],
            "user_answer": user_answer,
            "is_correct": is_correct,
        })

    total = len(QUIZ_QUESTIONS)
    percentage = round((score / total) * 100, 1)

    # Determine awareness level
    if score <= 3:
        awareness_level = 'needs_improvement'
    elif score <= 7:
        awareness_level = 'moderate'
    else:
        awareness_level = 'good'

    # Save to database
    quiz_data = {
        'score': score,
        'total_questions': total,
        'percentage': percentage,
        'awareness_level': awareness_level,
    }
    serializer = QuizResultSerializer(data=quiz_data)
    if serializer.is_valid():
        serializer.save()

    return Response({
        "score": score,
        "total_questions": total,
        "percentage": percentage,
        "awareness_level": awareness_level,
        "details": results_detail,
    })


@api_view(['GET'])
def quiz_statistics(request):
    """
    GET /api/quiz/statistics/
    Returns aggregated quiz statistics for the dashboard.
    """
    total = QuizResult.objects.count()

    if total == 0:
        return Response({
            "total_attempts": 0,
            "average_score": 0,
            "average_percentage": 0,
            "good_percentage": 0,
            "moderate_percentage": 0,
            "needs_improvement_percentage": 0,
            "level_distribution": {},
        })

    avg_score = QuizResult.objects.aggregate(avg=Avg('score'))['avg'] or 0
    avg_percentage = QuizResult.objects.aggregate(avg=Avg('percentage'))['avg'] or 0

    level_counts = (
        QuizResult.objects
        .values('awareness_level')
        .annotate(count=Count('id'))
    )
    level_dict = {item['awareness_level']: item['count'] for item in level_counts}

    good = level_dict.get('good', 0)
    moderate = level_dict.get('moderate', 0)
    needs = level_dict.get('needs_improvement', 0)

    return Response({
        "total_attempts": total,
        "average_score": round(avg_score, 1),
        "average_percentage": round(avg_percentage, 1),
        "good_percentage": round((good / total) * 100, 1),
        "moderate_percentage": round((moderate / total) * 100, 1),
        "needs_improvement_percentage": round((needs / total) * 100, 1),
        "level_distribution": level_dict,
    })
