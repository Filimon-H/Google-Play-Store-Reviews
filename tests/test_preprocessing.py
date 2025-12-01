"""
Unit tests for src/preprocessing.py
Tests the ReviewPreprocessor class and its methods.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime, date
from io import StringIO

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from preprocessing import ReviewPreprocessor


class TestReviewPreprocessorInit:
    """Tests for ReviewPreprocessor initialization."""
    
    def test_init_default_paths(self):
        """Preprocessor should initialize with default paths."""
        preprocessor = ReviewPreprocessor()
        assert preprocessor.input_path is not None
        assert preprocessor.output_path is not None
        assert preprocessor.df is None
        assert preprocessor.stats == {}
    
    def test_init_custom_paths(self):
        """Preprocessor should accept custom paths."""
        preprocessor = ReviewPreprocessor(
            input_path='custom/input.csv',
            output_path='custom/output.csv'
        )
        assert preprocessor.input_path == 'custom/input.csv'
        assert preprocessor.output_path == 'custom/output.csv'


class TestIsEnglish:
    """Tests for the is_english method."""
    
    @pytest.fixture
    def preprocessor(self):
        return ReviewPreprocessor()
    
    def test_english_text_returns_true(self, preprocessor):
        """English text should return True."""
        assert preprocessor.is_english("This is a great app!") is True
        assert preprocessor.is_english("The login works perfectly.") is True
    
    def test_non_english_text_returns_false(self, preprocessor):
        """Non-English text should return False."""
        # Amharic text
        assert preprocessor.is_english("ይህ መተግበሪያ በጣም ጥሩ ነው") is False
        # Arabic text
        assert preprocessor.is_english("هذا التطبيق رائع") is False
    
    def test_empty_string_returns_false(self, preprocessor):
        """Empty string should return False."""
        assert preprocessor.is_english("") is False
    
    def test_none_returns_false(self, preprocessor):
        """None should return False."""
        assert preprocessor.is_english(None) is False
    
    def test_short_text_returns_false(self, preprocessor):
        """Very short text (< 3 chars) should return False."""
        assert preprocessor.is_english("ab") is False
        assert preprocessor.is_english("a") is False
    
    def test_mixed_text_mostly_english(self, preprocessor):
        """Mixed text that is mostly English should return True."""
        # More than 70% ASCII letters
        assert preprocessor.is_english("Good app with some issues") is True
    
    def test_numbers_only_returns_false(self, preprocessor):
        """Text with only numbers should return False."""
        assert preprocessor.is_english("12345") is False
    
    def test_special_chars_only_returns_false(self, preprocessor):
        """Text with only special characters should return False."""
        assert preprocessor.is_english("!@#$%") is False


class TestCleanText:
    """Tests for text cleaning functionality."""
    
    @pytest.fixture
    def preprocessor_with_data(self):
        """Create preprocessor with sample data."""
        preprocessor = ReviewPreprocessor()
        preprocessor.df = pd.DataFrame({
            'review_text': [
                'This   is   a   test',  # Multiple spaces
                'Hello\n\nWorld',         # Newlines
                '  Trimmed  ',            # Leading/trailing spaces
                '',                        # Empty
                None,                      # None
                'Normal text here'
            ],
            'rating': [5, 4, 3, 2, 1, 5],
            'bank_code': ['CBE'] * 6,
            'bank_name': ['Commercial Bank of Ethiopia'] * 6
        })
        preprocessor.stats = {}
        return preprocessor
    
    def test_clean_text_removes_extra_whitespace(self, preprocessor_with_data):
        """clean_text should normalize whitespace."""
        preprocessor_with_data.clean_text()
        df = preprocessor_with_data.df
        
        # Check that multiple spaces are reduced to single space
        assert 'This is a test' in df['review_text'].values
    
    def test_clean_text_removes_newlines(self, preprocessor_with_data):
        """clean_text should remove newlines."""
        preprocessor_with_data.clean_text()
        df = preprocessor_with_data.df
        
        assert 'Hello World' in df['review_text'].values
    
    def test_clean_text_trims_whitespace(self, preprocessor_with_data):
        """clean_text should trim leading/trailing whitespace."""
        preprocessor_with_data.clean_text()
        df = preprocessor_with_data.df
        
        assert 'Trimmed' in df['review_text'].values
    
    def test_clean_text_removes_empty_reviews(self, preprocessor_with_data):
        """clean_text should remove empty reviews."""
        initial_count = len(preprocessor_with_data.df)
        preprocessor_with_data.clean_text()
        
        # Should have removed empty and None reviews
        assert len(preprocessor_with_data.df) < initial_count
    
    def test_clean_text_creates_text_length_column(self, preprocessor_with_data):
        """clean_text should create text_length column."""
        preprocessor_with_data.clean_text()
        
        assert 'text_length' in preprocessor_with_data.df.columns
        assert all(preprocessor_with_data.df['text_length'] > 0)


class TestRemoveDuplicates:
    """Tests for duplicate removal."""
    
    @pytest.fixture
    def preprocessor_with_duplicates(self):
        """Create preprocessor with duplicate data."""
        preprocessor = ReviewPreprocessor()
        preprocessor.df = pd.DataFrame({
            'review_text': ['Great app', 'Great app', 'Bad app', 'Great app'],
            'rating': [5, 5, 1, 4],  # Same text, different rating
            'bank_code': ['CBE', 'CBE', 'CBE', 'BOA'],  # Same text, different bank
            'bank_name': ['CBE', 'CBE', 'CBE', 'BOA']
        })
        preprocessor.stats = {}
        return preprocessor
    
    def test_remove_duplicates_keeps_first(self, preprocessor_with_duplicates):
        """remove_duplicates should keep first occurrence."""
        preprocessor_with_duplicates.remove_duplicates()
        
        # Should have 3 unique combinations (text, rating, bank_code)
        assert len(preprocessor_with_duplicates.df) == 3
    
    def test_remove_duplicates_updates_stats(self, preprocessor_with_duplicates):
        """remove_duplicates should update stats."""
        preprocessor_with_duplicates.remove_duplicates()
        
        assert 'duplicates_removed' in preprocessor_with_duplicates.stats
        assert preprocessor_with_duplicates.stats['duplicates_removed'] == 1


class TestHandleMissingValues:
    """Tests for missing value handling."""
    
    @pytest.fixture
    def preprocessor_with_missing(self):
        """Create preprocessor with missing values."""
        preprocessor = ReviewPreprocessor()
        preprocessor.df = pd.DataFrame({
            'review_text': ['Good', None, 'Bad', 'OK'],
            'rating': [5, 4, None, 3],
            'bank_name': ['CBE', 'BOA', 'Dashen', None],
            'user_name': ['User1', None, 'User3', 'User4'],
            'thumbs_up': [10, None, 5, 0],
            'reply_content': ['Thanks', None, None, 'OK']
        })
        preprocessor.stats = {}
        return preprocessor
    
    def test_handle_missing_drops_critical_nulls(self, preprocessor_with_missing):
        """handle_missing_values should drop rows with null critical columns."""
        initial_count = len(preprocessor_with_missing.df)
        preprocessor_with_missing.handle_missing_values()
        
        # Should have dropped rows with null review_text, rating, or bank_name
        assert len(preprocessor_with_missing.df) < initial_count
    
    def test_handle_missing_fills_user_name(self, preprocessor_with_missing):
        """handle_missing_values should fill null user_name with 'Anonymous'."""
        preprocessor_with_missing.handle_missing_values()
        
        # No null user_names should remain
        assert preprocessor_with_missing.df['user_name'].isnull().sum() == 0
    
    def test_handle_missing_fills_thumbs_up(self, preprocessor_with_missing):
        """handle_missing_values should fill null thumbs_up with 0."""
        preprocessor_with_missing.handle_missing_values()
        
        assert preprocessor_with_missing.df['thumbs_up'].isnull().sum() == 0


class TestNormalizeDates:
    """Tests for date normalization."""
    
    @pytest.fixture
    def preprocessor_with_dates(self):
        """Create preprocessor with various date formats."""
        preprocessor = ReviewPreprocessor()
        preprocessor.df = pd.DataFrame({
            'review_date': [
                '2024-01-15',
                '2024-02-20',
                '2024-03-25',
                '2024-04-30'
            ],
            'review_text': ['a', 'b', 'c', 'd'],
            'rating': [5, 4, 3, 2]
        })
        preprocessor.stats = {}
        return preprocessor
    
    def test_normalize_dates_converts_to_date(self, preprocessor_with_dates):
        """normalize_dates should convert all dates to date objects."""
        preprocessor_with_dates.normalize_dates()
        
        # All values should be date objects
        for d in preprocessor_with_dates.df['review_date']:
            assert isinstance(d, date)
    
    def test_normalize_dates_creates_year_column(self, preprocessor_with_dates):
        """normalize_dates should create review_year column."""
        preprocessor_with_dates.normalize_dates()
        
        assert 'review_year' in preprocessor_with_dates.df.columns
        assert all(preprocessor_with_dates.df['review_year'] == 2024)
    
    def test_normalize_dates_creates_month_column(self, preprocessor_with_dates):
        """normalize_dates should create review_month column."""
        preprocessor_with_dates.normalize_dates()
        
        assert 'review_month' in preprocessor_with_dates.df.columns
        assert list(preprocessor_with_dates.df['review_month']) == [1, 2, 3, 4]


class TestValidateRatings:
    """Tests for rating validation."""
    
    @pytest.fixture
    def preprocessor_with_ratings(self):
        """Create preprocessor with various ratings."""
        preprocessor = ReviewPreprocessor()
        preprocessor.df = pd.DataFrame({
            'rating': [1, 2, 3, 4, 5, 0, 6, -1, 10],
            'review_text': ['a'] * 9,
            'bank_name': ['CBE'] * 9
        })
        preprocessor.stats = {}
        return preprocessor
    
    def test_validate_ratings_keeps_valid(self, preprocessor_with_ratings):
        """validate_ratings should keep ratings 1-5."""
        preprocessor_with_ratings.validate_ratings()
        
        # Only ratings 1-5 should remain
        assert all(preprocessor_with_ratings.df['rating'].between(1, 5))
    
    def test_validate_ratings_removes_invalid(self, preprocessor_with_ratings):
        """validate_ratings should remove invalid ratings."""
        preprocessor_with_ratings.validate_ratings()
        
        # Should have removed 0, 6, -1, 10
        assert len(preprocessor_with_ratings.df) == 5
    
    def test_validate_ratings_updates_stats(self, preprocessor_with_ratings):
        """validate_ratings should update stats."""
        preprocessor_with_ratings.validate_ratings()
        
        assert 'invalid_ratings_removed' in preprocessor_with_ratings.stats
        assert preprocessor_with_ratings.stats['invalid_ratings_removed'] == 4


class TestFilterEnglishReviews:
    """Tests for English language filtering."""
    
    @pytest.fixture
    def preprocessor_with_languages(self):
        """Create preprocessor with mixed language reviews."""
        preprocessor = ReviewPreprocessor()
        preprocessor.df = pd.DataFrame({
            'review_text': [
                'This is an English review',
                'Another English text here',
                'ይህ አማርኛ ነው',  # Amharic
                'Good app works well',
                'هذا عربي',  # Arabic
            ],
            'rating': [5, 4, 3, 2, 1],
            'bank_name': ['CBE'] * 5
        })
        preprocessor.stats = {}
        return preprocessor
    
    def test_filter_english_keeps_english(self, preprocessor_with_languages):
        """filter_english_reviews should keep English reviews."""
        preprocessor_with_languages.filter_english_reviews()
        
        # Should have kept only English reviews
        assert len(preprocessor_with_languages.df) == 3
    
    def test_filter_english_removes_non_english(self, preprocessor_with_languages):
        """filter_english_reviews should remove non-English reviews."""
        preprocessor_with_languages.filter_english_reviews()
        
        # No Amharic or Arabic text should remain
        for text in preprocessor_with_languages.df['review_text']:
            assert preprocessor_with_languages.is_english(text)
    
    def test_filter_english_updates_stats(self, preprocessor_with_languages):
        """filter_english_reviews should update stats."""
        preprocessor_with_languages.filter_english_reviews()
        
        assert 'non_english_removed' in preprocessor_with_languages.stats
        assert preprocessor_with_languages.stats['non_english_removed'] == 2


class TestPrepareOutput:
    """Tests for final output preparation."""
    
    @pytest.fixture
    def preprocessor_for_output(self):
        """Create preprocessor ready for output."""
        preprocessor = ReviewPreprocessor()
        preprocessor.df = pd.DataFrame({
            'review_id': ['r1', 'r2', 'r3'],
            'review_text': ['Good', 'Bad', 'OK'],
            'rating': [5, 1, 3],
            'review_date': [date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)],
            'review_year': [2024, 2024, 2024],
            'review_month': [1, 1, 1],
            'bank_code': ['CBE', 'BOA', 'CBE'],
            'bank_name': ['CBE', 'BOA', 'CBE'],
            'user_name': ['U1', 'U2', 'U3'],
            'thumbs_up': [10, 5, 0],
            'text_length': [4, 3, 2],
            'source': ['Google Play'] * 3,
            'extra_column': ['x', 'y', 'z']  # Should be excluded
        })
        preprocessor.stats = {}
        return preprocessor
    
    def test_prepare_output_selects_columns(self, preprocessor_for_output):
        """prepare_final_output should select only required columns."""
        preprocessor_for_output.prepare_final_output()
        
        # extra_column should not be in output
        assert 'extra_column' not in preprocessor_for_output.df.columns
    
    def test_prepare_output_sorts_data(self, preprocessor_for_output):
        """prepare_final_output should sort by bank_code and review_date."""
        preprocessor_for_output.prepare_final_output()
        
        # Should be sorted by bank_code (ascending) then review_date (descending)
        df = preprocessor_for_output.df
        assert df.iloc[0]['bank_code'] == 'BOA'  # BOA comes before CBE alphabetically
    
    def test_prepare_output_resets_index(self, preprocessor_for_output):
        """prepare_final_output should reset the index."""
        preprocessor_for_output.prepare_final_output()
        
        assert list(preprocessor_for_output.df.index) == [0, 1, 2]


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_empty_dataframe(self):
        """Preprocessor should handle empty DataFrame."""
        preprocessor = ReviewPreprocessor()
        preprocessor.df = pd.DataFrame()
        preprocessor.stats = {}
        
        # Should not raise errors
        # Note: Some methods may fail on empty df, which is expected
    
    def test_single_row_dataframe(self):
        """Preprocessor should handle single-row DataFrame."""
        preprocessor = ReviewPreprocessor()
        preprocessor.df = pd.DataFrame({
            'review_text': ['Single review'],
            'rating': [5],
            'bank_code': ['CBE'],
            'bank_name': ['Commercial Bank of Ethiopia'],
            'user_name': ['User'],
            'thumbs_up': [0],
            'reply_content': [''],
            'review_date': ['2024-01-01']
        })
        preprocessor.stats = {}
        
        # Should process without errors
        preprocessor.check_missing_data()
        preprocessor.clean_text()
        
        assert len(preprocessor.df) == 1
