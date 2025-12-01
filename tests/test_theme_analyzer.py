"""
Unit tests for src/theme_analyzer.py
Tests the ThemeAnalyzer class and its methods.
"""

import pytest
import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from theme_analyzer import ThemeAnalyzer


class TestThemeAnalyzerInit:
    """Tests for ThemeAnalyzer initialization."""
    
    def test_init_creates_instance(self):
        """Should create ThemeAnalyzer instance."""
        analyzer = ThemeAnalyzer()
        
        assert analyzer is not None
    
    def test_init_has_theme_keywords(self):
        """Should have theme keywords loaded."""
        analyzer = ThemeAnalyzer()
        
        assert analyzer.theme_keywords is not None
        assert isinstance(analyzer.theme_keywords, dict)
        assert len(analyzer.theme_keywords) > 0
    
    def test_init_has_tfidf_vectorizer(self):
        """Should have TF-IDF vectorizer initialized."""
        analyzer = ThemeAnalyzer()
        
        assert analyzer.tfidf_vectorizer is not None


class TestPreprocessText:
    """Tests for text preprocessing."""
    
    @pytest.fixture
    def analyzer(self):
        return ThemeAnalyzer()
    
    def test_preprocess_lowercase(self, analyzer):
        """Should convert text to lowercase."""
        result = analyzer.preprocess_text("HELLO WORLD")
        
        assert result == result.lower()
    
    def test_preprocess_removes_special_chars(self, analyzer):
        """Should remove special characters."""
        result = analyzer.preprocess_text("Hello! How are you?")
        
        assert '!' not in result
        assert '?' not in result
    
    def test_preprocess_empty_string(self, analyzer):
        """Should handle empty string."""
        result = analyzer.preprocess_text("")
        
        assert result == ""
    
    def test_preprocess_none(self, analyzer):
        """Should handle None input."""
        result = analyzer.preprocess_text(None)
        
        assert result == ""
    
    def test_preprocess_numbers(self, analyzer):
        """Should remove numbers."""
        result = analyzer.preprocess_text("Version 1.2.3 released")
        
        assert '1' not in result
        assert '2' not in result
        assert '3' not in result
    
    def test_preprocess_whitespace(self, analyzer):
        """Should normalize whitespace."""
        result = analyzer.preprocess_text("Hello    World")
        
        assert '    ' not in result


class TestIdentifyThemes:
    """Tests for theme identification."""
    
    @pytest.fixture
    def analyzer(self):
        return ThemeAnalyzer()
    
    def test_identify_login_theme(self, analyzer):
        """Should identify Account Access Issues theme."""
        result = analyzer.identify_themes("I can't login to my account")
        
        assert 'Account Access Issues' in result['themes']
    
    def test_identify_transaction_theme(self, analyzer):
        """Should identify Transaction Performance theme."""
        result = analyzer.identify_themes("The transfer is very slow")
        
        assert 'Transaction Performance' in result['themes']
    
    def test_identify_technical_theme(self, analyzer):
        """Should identify Technical Issues theme."""
        result = analyzer.identify_themes("The app keeps crashing")
        
        assert 'Technical Issues' in result['themes']
    
    def test_identify_ui_theme(self, analyzer):
        """Should identify User Interface theme."""
        result = analyzer.identify_themes("The interface is confusing")
        
        assert 'User Interface & Experience' in result['themes']
    
    def test_identify_support_theme(self, analyzer):
        """Should identify Customer Support theme."""
        result = analyzer.identify_themes("Customer support never responds")
        
        assert 'Customer Support' in result['themes']
    
    def test_identify_feature_theme(self, analyzer):
        """Should identify Feature Requests theme."""
        result = analyzer.identify_themes("Please add fingerprint feature")
        
        assert 'Feature Requests' in result['themes']
    
    def test_identify_security_theme(self, analyzer):
        """Should identify Security theme."""
        result = analyzer.identify_themes("Is this app secure?")
        
        assert 'Security & Privacy' in result['themes']
    
    def test_identify_multiple_themes(self, analyzer):
        """Should identify multiple themes in one text."""
        result = analyzer.identify_themes("Login is slow and the app crashes")
        
        assert len(result['themes']) >= 2
    
    def test_identify_no_theme(self, analyzer):
        """Should return 'Other' when no theme matches."""
        result = analyzer.identify_themes("xyz abc 123")
        
        assert result['primary_theme'] == 'Other'
    
    def test_identify_empty_string(self, analyzer):
        """Should handle empty string."""
        result = analyzer.identify_themes("")
        
        assert result['themes'] == []
        assert result['primary_theme'] == 'Unknown'
    
    def test_identify_none(self, analyzer):
        """Should handle None input."""
        result = analyzer.identify_themes(None)
        
        assert result['themes'] == []
        assert result['primary_theme'] == 'Unknown'
    
    def test_result_has_matched_keywords(self, analyzer):
        """Result should include matched keywords."""
        result = analyzer.identify_themes("The login password reset is broken")
        
        assert 'matched_keywords' in result
        assert len(result['matched_keywords']) > 0
    
    def test_primary_theme_is_most_matched(self, analyzer):
        """Primary theme should be the one with most keyword matches."""
        # Text with more login-related keywords
        result = analyzer.identify_themes("login password authentication access account")
        
        assert result['primary_theme'] == 'Account Access Issues'


class TestExtractKeywordsTfidf:
    """Tests for TF-IDF keyword extraction."""
    
    @pytest.fixture
    def analyzer(self):
        return ThemeAnalyzer()
    
    def test_extract_keywords_returns_list(self, analyzer):
        """Should return a list of keyword lists."""
        texts = [
            "Great banking app with fast transfers",
            "Bad app crashes frequently",
            "Okay app needs improvement"
        ]
        result = analyzer.extract_keywords_tfidf(texts)
        
        assert isinstance(result, list)
        assert len(result) == len(texts)
    
    def test_extract_keywords_each_item_is_list(self, analyzer):
        """Each item should be a list of keywords."""
        texts = [
            "Great banking application",
            "Bad mobile banking experience"
        ]
        result = analyzer.extract_keywords_tfidf(texts)
        
        for keywords in result:
            assert isinstance(keywords, list)
    
    def test_extract_keywords_respects_top_n(self, analyzer):
        """Should respect top_n parameter."""
        texts = [
            "This is a test with many different words to extract from banking",
            "Another test document with banking features and mobile app",
            "Third document about transfers and payments in banking"
        ]
        result = analyzer.extract_keywords_tfidf(texts, top_n=3)
        
        # Each result should have at most top_n keywords
        for keywords in result:
            assert len(keywords) <= 3
    
    def test_extract_keywords_with_sufficient_documents(self, analyzer):
        """Should extract keywords from sufficient documents."""
        texts = [
            "Banking app login feature works great",
            "Mobile banking transfer is fast",
            "Banking application crashes sometimes",
            "Login to banking app is slow"
        ]
        result = analyzer.extract_keywords_tfidf(texts)
        
        assert isinstance(result, list)
        assert len(result) == 4


class TestAnalyzeDataFrame:
    """Tests for DataFrame theme analysis."""
    
    @pytest.fixture
    def analyzer(self):
        return ThemeAnalyzer()
    
    @pytest.fixture
    def sample_df(self):
        """Sample DataFrame with reviews."""
        return pd.DataFrame({
            'review_text': [
                'Cannot login to my account',
                'Transfer is very slow',
                'App crashes frequently',
                'Great app works well',
                'Please add more features'
            ],
            'rating': [1, 2, 1, 5, 3],
            'bank_name': ['CBE', 'BOA', 'Dashen', 'CBE', 'BOA']
        })
    
    def test_analyze_dataframe_returns_df(self, analyzer, sample_df):
        """analyze_dataframe should return a DataFrame."""
        result = analyzer.analyze_dataframe(sample_df)
        
        assert isinstance(result, pd.DataFrame)
    
    def test_analyze_dataframe_adds_themes_column(self, analyzer, sample_df):
        """analyze_dataframe should add themes column."""
        result = analyzer.analyze_dataframe(sample_df)
        
        assert 'themes' in result.columns
    
    def test_analyze_dataframe_adds_primary_theme_column(self, analyzer, sample_df):
        """analyze_dataframe should add primary_theme column."""
        result = analyzer.analyze_dataframe(sample_df)
        
        assert 'primary_theme' in result.columns
    
    def test_analyze_dataframe_adds_matched_keywords_column(self, analyzer, sample_df):
        """analyze_dataframe should add matched_keywords column."""
        result = analyzer.analyze_dataframe(sample_df)
        
        assert 'matched_keywords' in result.columns
    
    def test_analyze_dataframe_adds_tfidf_keywords_column(self, analyzer, sample_df):
        """analyze_dataframe should add tfidf_keywords column."""
        result = analyzer.analyze_dataframe(sample_df)
        
        assert 'tfidf_keywords' in result.columns
    
    def test_analyze_dataframe_preserves_original_columns(self, analyzer, sample_df):
        """analyze_dataframe should preserve original columns."""
        result = analyzer.analyze_dataframe(sample_df)
        
        assert 'review_text' in result.columns
        assert 'rating' in result.columns
        assert 'bank_name' in result.columns
    
    def test_analyze_dataframe_correct_length(self, analyzer, sample_df):
        """analyze_dataframe should return same number of rows."""
        result = analyzer.analyze_dataframe(sample_df)
        
        assert len(result) == len(sample_df)
    
    def test_analyze_dataframe_themes_are_lists(self, analyzer, sample_df):
        """themes column should contain lists."""
        result = analyzer.analyze_dataframe(sample_df)
        
        for themes in result['themes']:
            assert isinstance(themes, list)


class TestGetThemeSentimentCorrelation:
    """Tests for theme-sentiment correlation analysis."""
    
    @pytest.fixture
    def analyzer(self):
        return ThemeAnalyzer()
    
    @pytest.fixture
    def df_with_sentiment(self):
        """DataFrame with themes and sentiment."""
        return pd.DataFrame({
            'review_text': [
                'Login is broken',
                'Login works great',
                'App crashes',
                'App is stable'
            ],
            'themes': [
                ['Account Access Issues'],
                ['Account Access Issues'],
                ['Technical Issues'],
                ['Technical Issues']
            ],
            'sentiment_label_vader': ['NEGATIVE', 'POSITIVE', 'NEGATIVE', 'POSITIVE'],
            'bank_name': ['CBE', 'CBE', 'BOA', 'BOA']
        })
    
    def test_correlation_returns_dataframe(self, analyzer, df_with_sentiment):
        """get_theme_sentiment_correlation should return DataFrame."""
        result = analyzer.get_theme_sentiment_correlation(df_with_sentiment)
        
        assert isinstance(result, pd.DataFrame)
    
    def test_correlation_has_required_columns(self, analyzer, df_with_sentiment):
        """Result should have required columns."""
        result = analyzer.get_theme_sentiment_correlation(df_with_sentiment)
        
        assert 'theme' in result.columns
        assert 'positive_pct' in result.columns
        assert 'negative_pct' in result.columns
    
    def test_correlation_no_sentiment_column(self, analyzer):
        """Should return None if no sentiment column exists."""
        df = pd.DataFrame({
            'review_text': ['test'],
            'themes': [['Technical Issues']]
        })
        
        result = analyzer.get_theme_sentiment_correlation(df)
        
        assert result is None


class TestEdgeCases:
    """Tests for edge cases."""
    
    @pytest.fixture
    def analyzer(self):
        return ThemeAnalyzer()
    
    def test_identify_themes_empty_text(self, analyzer):
        """Should handle empty text in identify_themes."""
        result = analyzer.identify_themes('')
        
        assert result['themes'] == []
        assert result['primary_theme'] == 'Unknown'
    
    def test_identify_themes_none(self, analyzer):
        """Should handle None in identify_themes."""
        result = analyzer.identify_themes(None)
        
        assert result['themes'] == []
        assert result['primary_theme'] == 'Unknown'
    
    def test_multiple_reviews_dataframe(self, analyzer):
        """Should handle DataFrame with multiple reviews."""
        df = pd.DataFrame({
            'review_text': [
                'Login is not working properly today',
                'Transfer is very slow and crashes',
                'App crashes when I open it daily',
                'Login feature needs improvement badly',
                'Transfer money takes too long always'
            ]
        })
        
        result = analyzer.analyze_dataframe(df)
        
        assert len(result) == 5
        assert 'themes' in result.columns
    
    def test_dataframe_with_none_values(self, analyzer):
        """Should handle DataFrame with None values."""
        df = pd.DataFrame({
            'review_text': [
                'Good app with login feature',
                None,
                'Bad app crashes often'
            ]
        })
        
        result = analyzer.analyze_dataframe(df)
        
        assert len(result) == 3
    
    def test_very_long_text(self, analyzer):
        """Should handle very long text."""
        long_text = "login " * 1000
        result = analyzer.identify_themes(long_text)
        
        assert 'Account Access Issues' in result['themes']
    
    def test_unicode_text(self, analyzer):
        """Should handle unicode text."""
        result = analyzer.identify_themes("Login 登录 تسجيل الدخول")
        
        # Should not crash
        assert 'themes' in result
    
    def test_case_insensitive_matching(self, analyzer):
        """Theme matching should be case-insensitive."""
        result1 = analyzer.identify_themes("LOGIN")
        result2 = analyzer.identify_themes("login")
        result3 = analyzer.identify_themes("Login")
        
        # All should identify the same theme
        assert result1['primary_theme'] == result2['primary_theme']
        assert result2['primary_theme'] == result3['primary_theme']
