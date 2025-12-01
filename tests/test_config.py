"""
Unit tests for src/config.py
Tests configuration values and structure.
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import (
    APP_IDS, BANK_NAMES, SCRAPING_CONFIG, DATA_PATHS,
    DB_CONFIG, SENTIMENT_CONFIG, THEME_CONFIG, VIZ_CONFIG, THEME_KEYWORDS
)


class TestAppIDs:
    """Tests for APP_IDS configuration."""
    
    def test_app_ids_is_dict(self):
        """APP_IDS should be a dictionary."""
        assert isinstance(APP_IDS, dict)
    
    def test_app_ids_has_required_banks(self):
        """APP_IDS should contain CBE, BOA, and Dashen."""
        required_banks = ['CBE', 'BOA', 'Dashen']
        for bank in required_banks:
            assert bank in APP_IDS, f"Missing bank: {bank}"
    
    def test_app_ids_values_are_strings(self):
        """All app IDs should be strings."""
        for bank, app_id in APP_IDS.items():
            assert isinstance(app_id, str), f"App ID for {bank} is not a string"
    
    def test_app_ids_values_not_empty(self):
        """App IDs should not be empty strings."""
        for bank, app_id in APP_IDS.items():
            assert len(app_id) > 0, f"App ID for {bank} is empty"


class TestBankNames:
    """Tests for BANK_NAMES configuration."""
    
    def test_bank_names_is_dict(self):
        """BANK_NAMES should be a dictionary."""
        assert isinstance(BANK_NAMES, dict)
    
    def test_bank_names_matches_app_ids_keys(self):
        """BANK_NAMES keys should match APP_IDS keys."""
        assert set(BANK_NAMES.keys()) == set(APP_IDS.keys())
    
    def test_bank_names_values_are_strings(self):
        """All bank names should be strings."""
        for code, name in BANK_NAMES.items():
            assert isinstance(name, str), f"Bank name for {code} is not a string"
    
    def test_bank_names_not_empty(self):
        """Bank names should not be empty."""
        for code, name in BANK_NAMES.items():
            assert len(name) > 0, f"Bank name for {code} is empty"


class TestScrapingConfig:
    """Tests for SCRAPING_CONFIG."""
    
    def test_scraping_config_is_dict(self):
        """SCRAPING_CONFIG should be a dictionary."""
        assert isinstance(SCRAPING_CONFIG, dict)
    
    def test_reviews_per_bank_is_positive_int(self):
        """reviews_per_bank should be a positive integer."""
        assert isinstance(SCRAPING_CONFIG['reviews_per_bank'], int)
        assert SCRAPING_CONFIG['reviews_per_bank'] > 0
    
    def test_max_retries_is_positive_int(self):
        """max_retries should be a positive integer."""
        assert isinstance(SCRAPING_CONFIG['max_retries'], int)
        assert SCRAPING_CONFIG['max_retries'] > 0
    
    def test_lang_is_string(self):
        """lang should be a string."""
        assert isinstance(SCRAPING_CONFIG['lang'], str)
        assert len(SCRAPING_CONFIG['lang']) == 2  # Language codes are 2 chars
    
    def test_country_is_string(self):
        """country should be a string."""
        assert isinstance(SCRAPING_CONFIG['country'], str)
        assert len(SCRAPING_CONFIG['country']) == 2  # Country codes are 2 chars


class TestDataPaths:
    """Tests for DATA_PATHS configuration."""
    
    def test_data_paths_is_dict(self):
        """DATA_PATHS should be a dictionary."""
        assert isinstance(DATA_PATHS, dict)
    
    def test_required_paths_exist(self):
        """Required path keys should exist."""
        required_keys = ['raw', 'processed', 'raw_reviews', 'processed_reviews']
        for key in required_keys:
            assert key in DATA_PATHS, f"Missing path key: {key}"
    
    def test_paths_are_strings(self):
        """All paths should be strings."""
        for key, path in DATA_PATHS.items():
            assert isinstance(path, str), f"Path for {key} is not a string"
    
    def test_paths_not_empty(self):
        """Paths should not be empty."""
        for key, path in DATA_PATHS.items():
            assert len(path) > 0, f"Path for {key} is empty"


class TestDBConfig:
    """Tests for DB_CONFIG."""
    
    def test_db_config_is_dict(self):
        """DB_CONFIG should be a dictionary."""
        assert isinstance(DB_CONFIG, dict)
    
    def test_required_db_keys_exist(self):
        """Required database config keys should exist."""
        required_keys = ['host', 'database', 'user', 'password', 'port']
        for key in required_keys:
            assert key in DB_CONFIG, f"Missing DB config key: {key}"
    
    def test_db_values_are_strings(self):
        """All DB config values should be strings."""
        for key, value in DB_CONFIG.items():
            assert isinstance(value, str), f"DB config {key} is not a string"


class TestSentimentConfig:
    """Tests for SENTIMENT_CONFIG."""
    
    def test_sentiment_config_is_dict(self):
        """SENTIMENT_CONFIG should be a dictionary."""
        assert isinstance(SENTIMENT_CONFIG, dict)
    
    def test_model_is_string(self):
        """model should be a string."""
        assert isinstance(SENTIMENT_CONFIG['model'], str)
        assert len(SENTIMENT_CONFIG['model']) > 0
    
    def test_use_vader_is_bool(self):
        """use_vader should be a boolean."""
        assert isinstance(SENTIMENT_CONFIG['use_vader'], bool)
    
    def test_batch_size_is_positive_int(self):
        """batch_size should be a positive integer."""
        assert isinstance(SENTIMENT_CONFIG['batch_size'], int)
        assert SENTIMENT_CONFIG['batch_size'] > 0


class TestThemeConfig:
    """Tests for THEME_CONFIG."""
    
    def test_theme_config_is_dict(self):
        """THEME_CONFIG should be a dictionary."""
        assert isinstance(THEME_CONFIG, dict)
    
    def test_num_themes_is_positive_int(self):
        """num_themes should be a positive integer."""
        assert isinstance(THEME_CONFIG['num_themes'], int)
        assert THEME_CONFIG['num_themes'] > 0
    
    def test_max_features_is_positive_int(self):
        """max_features should be a positive integer."""
        assert isinstance(THEME_CONFIG['max_features'], int)
        assert THEME_CONFIG['max_features'] > 0
    
    def test_ngram_range_is_tuple(self):
        """ngram_range should be a tuple of two integers."""
        assert isinstance(THEME_CONFIG['ngram_range'], tuple)
        assert len(THEME_CONFIG['ngram_range']) == 2
        assert all(isinstance(x, int) for x in THEME_CONFIG['ngram_range'])
    
    def test_min_df_is_positive_int(self):
        """min_df should be a positive integer."""
        assert isinstance(THEME_CONFIG['min_df'], int)
        assert THEME_CONFIG['min_df'] > 0


class TestThemeKeywords:
    """Tests for THEME_KEYWORDS."""
    
    def test_theme_keywords_is_dict(self):
        """THEME_KEYWORDS should be a dictionary."""
        assert isinstance(THEME_KEYWORDS, dict)
    
    def test_theme_keywords_not_empty(self):
        """THEME_KEYWORDS should have at least one theme."""
        assert len(THEME_KEYWORDS) > 0
    
    def test_theme_values_are_lists(self):
        """Each theme should have a list of keywords."""
        for theme, keywords in THEME_KEYWORDS.items():
            assert isinstance(keywords, list), f"Keywords for {theme} is not a list"
    
    def test_keywords_are_strings(self):
        """All keywords should be strings."""
        for theme, keywords in THEME_KEYWORDS.items():
            for keyword in keywords:
                assert isinstance(keyword, str), f"Keyword in {theme} is not a string"
    
    def test_keywords_not_empty(self):
        """Each theme should have at least one keyword."""
        for theme, keywords in THEME_KEYWORDS.items():
            assert len(keywords) > 0, f"Theme {theme} has no keywords"
    
    def test_expected_themes_exist(self):
        """Expected business themes should exist."""
        expected_themes = [
            'Account Access Issues',
            'Transaction Performance',
            'Technical Issues'
        ]
        for theme in expected_themes:
            assert theme in THEME_KEYWORDS, f"Missing expected theme: {theme}"


class TestVizConfig:
    """Tests for VIZ_CONFIG."""
    
    def test_viz_config_is_dict(self):
        """VIZ_CONFIG should be a dictionary."""
        assert isinstance(VIZ_CONFIG, dict)
    
    def test_figure_size_is_tuple(self):
        """figure_size should be a tuple."""
        assert isinstance(VIZ_CONFIG['figure_size'], tuple)
        assert len(VIZ_CONFIG['figure_size']) == 2
    
    def test_dpi_is_positive_int(self):
        """dpi should be a positive integer."""
        assert isinstance(VIZ_CONFIG['dpi'], int)
        assert VIZ_CONFIG['dpi'] > 0
