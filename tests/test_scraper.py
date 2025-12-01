"""
Unit tests for src/scraper.py
Tests the PlayStoreScraper class and its methods.

Note: These tests use mocked data to avoid actual API calls.
"""

import pytest
import pandas as pd
import sys
import os
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from scraper import PlayStoreScraper


class TestPlayStoreScraperInit:
    """Tests for PlayStoreScraper initialization."""
    
    def test_init_loads_config(self):
        """Scraper should initialize with config values."""
        scraper = PlayStoreScraper()
        
        assert scraper.app_ids is not None
        assert scraper.bank_names is not None
        assert isinstance(scraper.reviews_per_bank, int)
        assert scraper.reviews_per_bank > 0
    
    def test_init_has_required_banks(self):
        """Scraper should have all required banks."""
        scraper = PlayStoreScraper()
        
        required_banks = ['CBE', 'BOA', 'Dashen']
        for bank in required_banks:
            assert bank in scraper.app_ids
            assert bank in scraper.bank_names
    
    def test_init_lang_and_country(self):
        """Scraper should have language and country settings."""
        scraper = PlayStoreScraper()
        
        assert scraper.lang == 'en'
        assert scraper.country == 'et'


class TestProcessReviews:
    """Tests for the process_reviews method."""
    
    @pytest.fixture
    def scraper(self):
        return PlayStoreScraper()
    
    @pytest.fixture
    def sample_raw_reviews(self):
        """Sample raw review data as returned by google-play-scraper."""
        return [
            {
                'reviewId': 'review_001',
                'content': 'Great app, works perfectly!',
                'score': 5,
                'at': datetime(2024, 1, 15, 10, 30, 0),
                'userName': 'John Doe',
                'thumbsUpCount': 10,
                'replyContent': 'Thank you!',
                'reviewCreatedVersion': '1.0.0'
            },
            {
                'reviewId': 'review_002',
                'content': 'App crashes frequently',
                'score': 1,
                'at': datetime(2024, 1, 16, 14, 20, 0),
                'userName': 'Jane Smith',
                'thumbsUpCount': 5,
                'replyContent': None,
                'reviewCreatedVersion': '1.0.1'
            }
        ]
    
    def test_process_reviews_returns_list(self, scraper, sample_raw_reviews):
        """process_reviews should return a list."""
        result = scraper.process_reviews(sample_raw_reviews, 'CBE')
        
        assert isinstance(result, list)
    
    def test_process_reviews_correct_length(self, scraper, sample_raw_reviews):
        """process_reviews should return same number of items."""
        result = scraper.process_reviews(sample_raw_reviews, 'CBE')
        
        assert len(result) == len(sample_raw_reviews)
    
    def test_process_reviews_has_required_fields(self, scraper, sample_raw_reviews):
        """Processed reviews should have all required fields."""
        result = scraper.process_reviews(sample_raw_reviews, 'CBE')
        
        required_fields = [
            'review_id', 'review_text', 'rating', 'review_date',
            'user_name', 'thumbs_up', 'bank_code', 'bank_name', 'source'
        ]
        
        for review in result:
            for field in required_fields:
                assert field in review, f"Missing field: {field}"
    
    def test_process_reviews_correct_bank_code(self, scraper, sample_raw_reviews):
        """Processed reviews should have correct bank_code."""
        result = scraper.process_reviews(sample_raw_reviews, 'CBE')
        
        for review in result:
            assert review['bank_code'] == 'CBE'
    
    def test_process_reviews_correct_bank_name(self, scraper, sample_raw_reviews):
        """Processed reviews should have correct bank_name."""
        result = scraper.process_reviews(sample_raw_reviews, 'CBE')
        
        for review in result:
            assert review['bank_name'] == 'Commercial Bank of Ethiopia'
    
    def test_process_reviews_source_is_google_play(self, scraper, sample_raw_reviews):
        """Processed reviews should have 'Google Play' as source."""
        result = scraper.process_reviews(sample_raw_reviews, 'CBE')
        
        for review in result:
            assert review['source'] == 'Google Play'
    
    def test_process_reviews_extracts_content(self, scraper, sample_raw_reviews):
        """Processed reviews should extract review content."""
        result = scraper.process_reviews(sample_raw_reviews, 'CBE')
        
        assert result[0]['review_text'] == 'Great app, works perfectly!'
        assert result[1]['review_text'] == 'App crashes frequently'
    
    def test_process_reviews_extracts_rating(self, scraper, sample_raw_reviews):
        """Processed reviews should extract rating."""
        result = scraper.process_reviews(sample_raw_reviews, 'CBE')
        
        assert result[0]['rating'] == 5
        assert result[1]['rating'] == 1
    
    def test_process_reviews_empty_list(self, scraper):
        """process_reviews should handle empty list."""
        result = scraper.process_reviews([], 'CBE')
        
        assert result == []
    
    def test_process_reviews_missing_fields(self, scraper):
        """process_reviews should handle reviews with missing fields."""
        incomplete_reviews = [
            {
                'reviewId': 'review_003',
                # Missing 'content', 'score', etc.
            }
        ]
        
        result = scraper.process_reviews(incomplete_reviews, 'CBE')
        
        # Should still return a result with default values
        assert len(result) == 1
        assert result[0]['review_text'] == ''  # Default for missing content
        assert result[0]['rating'] == 0  # Default for missing score


class TestDisplaySampleReviews:
    """Tests for the display_sample_reviews method."""
    
    @pytest.fixture
    def scraper(self):
        return PlayStoreScraper()
    
    @pytest.fixture
    def sample_df(self):
        """Sample DataFrame with reviews."""
        return pd.DataFrame({
            'bank_code': ['CBE', 'CBE', 'BOA', 'BOA', 'Dashen'],
            'bank_name': [
                'Commercial Bank of Ethiopia',
                'Commercial Bank of Ethiopia',
                'Bank of Abyssinia',
                'Bank of Abyssinia',
                'Dashen Bank'
            ],
            'review_text': [
                'Great app!',
                'Works well',
                'Could be better',
                'Nice features',
                'Love it'
            ],
            'rating': [5, 4, 3, 4, 5],
            'review_date': ['2024-01-01'] * 5
        })
    
    def test_display_sample_reviews_no_error(self, scraper, sample_df, capsys):
        """display_sample_reviews should run without errors."""
        # Should not raise any exceptions
        scraper.display_sample_reviews(sample_df, n=2)
        
        captured = capsys.readouterr()
        assert 'Sample Reviews' in captured.out
    
    def test_display_sample_reviews_empty_df(self, scraper, capsys):
        """display_sample_reviews should handle empty DataFrame."""
        empty_df = pd.DataFrame({
            'bank_code': [],
            'bank_name': [],
            'review_text': [],
            'rating': [],
            'review_date': []
        })
        
        # Should not raise any exceptions
        scraper.display_sample_reviews(empty_df)


class TestGetAppInfo:
    """Tests for the get_app_info method with mocking."""
    
    @pytest.fixture
    def scraper(self):
        return PlayStoreScraper()
    
    @patch('scraper.app')
    def test_get_app_info_success(self, mock_app, scraper):
        """get_app_info should return app info on success."""
        mock_app.return_value = {
            'title': 'CBE Mobile Banking',
            'score': 4.5,
            'ratings': 10000,
            'reviews': 5000,
            'installs': '1,000,000+'
        }
        
        result = scraper.get_app_info('com.test.app')
        
        assert result is not None
        assert result['title'] == 'CBE Mobile Banking'
        assert result['score'] == 4.5
    
    @patch('scraper.app')
    def test_get_app_info_failure(self, mock_app, scraper):
        """get_app_info should return None on failure."""
        mock_app.side_effect = Exception("API Error")
        
        result = scraper.get_app_info('com.invalid.app')
        
        assert result is None


class TestScrapeReviews:
    """Tests for the scrape_reviews method with mocking."""
    
    @pytest.fixture
    def scraper(self):
        return PlayStoreScraper()
    
    @patch('scraper.reviews_all')
    def test_scrape_reviews_success(self, mock_reviews_all, scraper):
        """scrape_reviews should return reviews on success."""
        mock_reviews_all.return_value = [
            {'reviewId': '1', 'content': 'Test', 'score': 5},
            {'reviewId': '2', 'content': 'Test2', 'score': 4}
        ]
        
        result = scraper.scrape_reviews('com.test.app', count=100)
        
        assert len(result) == 2
    
    @patch('scraper.reviews_all')
    def test_scrape_reviews_failure_returns_empty(self, mock_reviews_all, scraper):
        """scrape_reviews should return empty list on failure after retries."""
        mock_reviews_all.side_effect = Exception("API Error")
        
        # Reduce retries for faster test
        scraper.max_retries = 1
        
        result = scraper.scrape_reviews('com.invalid.app', count=100)
        
        assert result == []


class TestEdgeCases:
    """Tests for edge cases."""
    
    @pytest.fixture
    def scraper(self):
        return PlayStoreScraper()
    
    def test_process_reviews_with_none_values(self, scraper):
        """process_reviews should handle None values in review data."""
        reviews_with_nones = [
            {
                'reviewId': None,
                'content': None,
                'score': None,
                'at': None,
                'userName': None,
                'thumbsUpCount': None,
                'replyContent': None,
                'reviewCreatedVersion': None
            }
        ]
        
        result = scraper.process_reviews(reviews_with_nones, 'CBE')
        
        # Should not raise and should return processed review
        assert len(result) == 1
    
    def test_process_reviews_with_unicode(self, scraper):
        """process_reviews should handle unicode characters."""
        unicode_reviews = [
            {
                'reviewId': 'review_unicode',
                'content': 'Great app! 👍 ⭐⭐⭐⭐⭐',
                'score': 5,
                'at': datetime.now(),
                'userName': 'User 日本語',
                'thumbsUpCount': 0,
                'replyContent': None,
                'reviewCreatedVersion': '1.0'
            }
        ]
        
        result = scraper.process_reviews(unicode_reviews, 'CBE')
        
        assert len(result) == 1
        assert '👍' in result[0]['review_text']
    
    def test_process_reviews_with_long_text(self, scraper):
        """process_reviews should handle very long review text."""
        long_text = 'A' * 10000  # 10,000 characters
        long_reviews = [
            {
                'reviewId': 'review_long',
                'content': long_text,
                'score': 3,
                'at': datetime.now(),
                'userName': 'User',
                'thumbsUpCount': 0,
                'replyContent': None,
                'reviewCreatedVersion': '1.0'
            }
        ]
        
        result = scraper.process_reviews(long_reviews, 'CBE')
        
        assert len(result) == 1
        assert len(result[0]['review_text']) == 10000
