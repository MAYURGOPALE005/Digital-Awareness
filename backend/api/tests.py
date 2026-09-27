from django.test import TestCase


class PageRoutesAndApiTests(TestCase):
    def test_required_pages_load(self):
        pages = [
            '/',
            '/learn/',
            '/quiz/',
            '/tips/',
            '/survey/',
            '/about/',
            '/dashboard/',
        ]

        for page in pages:
            response = self.client.get(page)
            self.assertEqual(response.status_code, 200, f"{page} should load successfully")

    def test_quiz_result_api_calculates_score_and_returns_level(self):
        payload = {
            'answers': {
                '1': 1,
                '2': 2,
                '3': 1,
                '4': 2,
                '5': 2,
                '6': 1,
                '7': 2,
                '8': 2,
                '9': 1,
                '10': 2,
            }
        }
        response = self.client.post('/api/quiz/result/', payload, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['score'], 10)
        self.assertEqual(response.json()['awareness_level'], 'good')

    def test_survey_api_accepts_submission(self):
        payload = {
            'age_group': '18_25',
            'internet_usage': 'daily',
            'platforms': 'Instagram, WhatsApp, Gmail',
            'privacy_awareness': 'moderately_aware',
            'password_practice': 'sometimes',
            'two_factor_auth': 'yes',
            'phishing_awareness': 'very_aware',
            'app_permissions': 'always',
            'social_media_privacy': 'sometimes',
            'online_payment_safety': 'always',
            'privacy_concern': 'Fake messages and scam calls.',
        }
        response = self.client.post('/api/survey/', payload, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('Survey submitted successfully', response.json()['message'])
