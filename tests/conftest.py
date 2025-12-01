"""
Pytest configuration and shared fixtures.
"""

import pytest
import pandas as pd
import sys
import os
from datetime import date, datetime

# Add src to path for all tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture
def sample_reviews_df():
    """
    Sample DataFrame with review data for testing.
    Contains a mix of positive, negative, and neutral reviews.
    """
    return pd.DataFrame({
        'review_id': ['r001', 'r002', 'r003', 'r004', 'r005'],
        'review_text': [
            'Great app, works perfectly!',
            'Terrible app, crashes all the time',
            'The app is okay, nothing special',
            'Love the new update, login is fast',
            'Cannot transfer money, very slow'
        ],
        'rating': [5, 1, 3, 5, 2],
        'review_date': [
            date(2024, 1, 1),
            date(2024, 1, 2),
            date(2024, 1, 3),
            date(2024, 1, 4),
            date(2024, 1, 5)
        ],
        'bank_code': ['CBE', 'BOA', 'Dashen', 'CBE', 'BOA'],
        'bank_name': [
            'Commercial Bank of Ethiopia',
            'Bank of Abyssinia',
            'Dashen Bank',
            'Commercial Bank of Ethiopia',
            'Bank of Abyssinia'
        ],
        'user_name': ['User1', 'User2', 'User3', 'User4', 'User5'],
        'thumbs_up': [10, 5, 0, 15, 3],
        'source': ['Google Play'] * 5
    })


@pytest.fixture
def sample_raw_reviews():
    """
    Sample raw review data as returned by google-play-scraper.
    """
    return [
        {
            'reviewId': 'raw_001',
            'content': 'Amazing banking app!',
            'score': 5,
            'at': datetime(2024, 1, 15, 10, 30, 0),
            'userName': 'Happy User',
            'thumbsUpCount': 25,
            'replyContent': 'Thank you for your feedback!',
            'reviewCreatedVersion': '2.0.0'
        },
        {
            'reviewId': 'raw_002',
            'content': 'App needs improvement',
            'score': 3,
            'at': datetime(2024, 1, 16, 14, 20, 0),
            'userName': 'Neutral User',
            'thumbsUpCount': 5,
            'replyContent': None,
            'reviewCreatedVersion': '2.0.1'
        },
        {
            'reviewId': 'raw_003',
            'content': 'Worst experience ever!',
            'score': 1,
            'at': datetime(2024, 1, 17, 9, 0, 0),
            'userName': 'Angry User',
            'thumbsUpCount': 50,
            'replyContent': 'We apologize for the inconvenience.',
            'reviewCreatedVersion': '2.0.0'
        }
    ]


@pytest.fixture
def sample_sentiment_df():
    """
    Sample DataFrame with sentiment analysis results.
    """
    return pd.DataFrame({
        'review_text': [
            'Great app!',
            'Terrible experience',
            'It works fine'
        ],
        'rating': [5, 1, 3],
        'bank_name': ['CBE', 'BOA', 'Dashen'],
        'sentiment_label_vader': ['POSITIVE', 'NEGATIVE', 'NEUTRAL'],
        'sentiment_score_vader': [0.85, 0.78, 0.45],
        'sentiment_label_distilbert': ['POSITIVE', 'NEGATIVE', 'POSITIVE'],
        'sentiment_score_distilbert': [0.92, 0.88, 0.65]
    })


@pytest.fixture
def sample_themes_df():
    """
    Sample DataFrame with theme analysis results.
    """
    return pd.DataFrame({
        'review_text': [
            'Cannot login to my account',
            'Transfer is very slow',
            'App crashes frequently',
            'Great user interface',
            'Please add more features'
        ],
        'themes': [
            ['Account Access Issues'],
            ['Transaction Performance'],
            ['Technical Issues'],
            ['User Interface & Experience'],
            ['Feature Requests']
        ],
        'primary_theme': [
            'Account Access Issues',
            'Transaction Performance',
            'Technical Issues',
            'User Interface & Experience',
            'Feature Requests'
        ],
        'matched_keywords': [
            ['login', 'account'],
            ['transfer', 'slow'],
            ['crash'],
            ['interface'],
            ['feature', 'add']
        ]
    })


@pytest.fixture
def empty_df():
    """
    Empty DataFrame for edge case testing.
    """
    return pd.DataFrame()


@pytest.fixture
def single_row_df():
    """
    Single-row DataFrame for edge case testing.
    """
    return pd.DataFrame({
        'review_text': ['Single review for testing'],
        'rating': [4],
        'bank_name': ['CBE']
    })


# Markers for slow tests
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
