"""
Unit tests for src/sentiment_analyzer.py
Tests the SentimentAnalyzer class and its methods.

Note: DistilBERT tests are marked as slow and can be skipped.
"""

import pytest
import pandas as pd
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sentiment_analyzer import SentimentAnalyzer


class TestSentimentAnalyzerInit:
    """Tests for SentimentAnalyzer initialization."""
    
    def test_init_vader(self):
        """Should initialize with VADER method."""
        analyzer = SentimentAnalyzer(method='vader')
        
        assert analyzer.method == 'vader'
        assert analyzer.model is not None
    
    def test_init_vader_case_insensitive(self):
        """Should accept method name in any case."""
        analyzer = SentimentAnalyzer(method='VADER')
        assert analyzer.method == 'vader'
        
        analyzer2 = SentimentAnalyzer(method='Vader')
        assert analyzer2.method == 'vader'
    
    def test_init_invalid_method_raises_error(self):
        """Should raise ValueError for invalid method."""
        with pytest.raises(ValueError) as excinfo:
            SentimentAnalyzer(method='invalid_method')
        
        assert 'Unknown method' in str(excinfo.value)


class TestVaderAnalyzeText:
    """Tests for VADER sentiment analysis."""
    
    @pytest.fixture
    def vader_analyzer(self):
        return SentimentAnalyzer(method='vader')
    
    def test_positive_text(self, vader_analyzer):
        """Positive text should return POSITIVE label."""
        result = vader_analyzer.analyze_text("This app is amazing! I love it!")
        
        assert result['label'] == 'POSITIVE'
        assert result['score'] > 0
    
    def test_negative_text(self, vader_analyzer):
        """Negative text should return NEGATIVE label."""
        result = vader_analyzer.analyze_text("This app is terrible. It crashes all the time.")
        
        assert result['label'] == 'NEGATIVE'
        assert result['score'] > 0
    
    def test_neutral_text(self, vader_analyzer):
        """Neutral text should return NEUTRAL label."""
        result = vader_analyzer.analyze_text("The app exists.")
        
        assert result['label'] == 'NEUTRAL'
    
    def test_empty_string(self, vader_analyzer):
        """Empty string should return NEUTRAL with score 0."""
        result = vader_analyzer.analyze_text("")
        
        assert result['label'] == 'NEUTRAL'
        assert result['score'] == 0.0
    
    def test_none_input(self, vader_analyzer):
        """None input should return NEUTRAL with score 0."""
        result = vader_analyzer.analyze_text(None)
        
        assert result['label'] == 'NEUTRAL'
        assert result['score'] == 0.0
    
    def test_whitespace_only(self, vader_analyzer):
        """Whitespace-only text should return NEUTRAL."""
        result = vader_analyzer.analyze_text("   \n\t  ")
        
        assert result['label'] == 'NEUTRAL'
        assert result['score'] == 0.0
    
    def test_result_has_compound_score(self, vader_analyzer):
        """VADER result should include compound score."""
        result = vader_analyzer.analyze_text("Great app!")
        
        assert 'compound' in result
        assert -1 <= result['compound'] <= 1
    
    def test_result_has_component_scores(self, vader_analyzer):
        """VADER result should include pos, neg, neu scores."""
        result = vader_analyzer.analyze_text("Good app with some issues")
        
        assert 'pos' in result
        assert 'neg' in result
        assert 'neu' in result
        
        # Scores should sum to approximately 1
        total = result['pos'] + result['neg'] + result['neu']
        assert abs(total - 1.0) < 0.01
    
    def test_strong_positive(self, vader_analyzer):
        """Very positive text should have high compound score."""
        result = vader_analyzer.analyze_text("AMAZING!!! Best app ever!!! I LOVE IT!!!")
        
        assert result['label'] == 'POSITIVE'
        assert result['compound'] > 0.5
    
    def test_strong_negative(self, vader_analyzer):
        """Very negative text should have low compound score."""
        result = vader_analyzer.analyze_text("TERRIBLE!!! Worst app ever!!! I HATE IT!!!")
        
        assert result['label'] == 'NEGATIVE'
        assert result['compound'] < -0.5
    
    def test_mixed_sentiment(self, vader_analyzer):
        """Mixed sentiment text should be analyzed."""
        result = vader_analyzer.analyze_text("The app is good but has some bad features")
        
        # Should return a valid result
        assert result['label'] in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
        assert 'score' in result


class TestAnalyzeDataFrame:
    """Tests for DataFrame sentiment analysis."""
    
    @pytest.fixture
    def vader_analyzer(self):
        return SentimentAnalyzer(method='vader')
    
    @pytest.fixture
    def sample_df(self):
        """Sample DataFrame with reviews."""
        return pd.DataFrame({
            'review_text': [
                'Great app, love it!',
                'Terrible, crashes constantly',
                'It works okay',
                'Amazing features!',
                'Worst app ever'
            ],
            'rating': [5, 1, 3, 5, 1],
            'bank_name': ['CBE', 'BOA', 'Dashen', 'CBE', 'BOA']
        })
    
    def test_analyze_dataframe_returns_df(self, vader_analyzer, sample_df):
        """analyze_dataframe should return a DataFrame."""
        result = vader_analyzer.analyze_dataframe(sample_df)
        
        assert isinstance(result, pd.DataFrame)
    
    def test_analyze_dataframe_adds_label_column(self, vader_analyzer, sample_df):
        """analyze_dataframe should add sentiment label column."""
        result = vader_analyzer.analyze_dataframe(sample_df)
        
        assert 'sentiment_label_vader' in result.columns
    
    def test_analyze_dataframe_adds_score_column(self, vader_analyzer, sample_df):
        """analyze_dataframe should add sentiment score column."""
        result = vader_analyzer.analyze_dataframe(sample_df)
        
        assert 'sentiment_score_vader' in result.columns
    
    def test_analyze_dataframe_preserves_original_columns(self, vader_analyzer, sample_df):
        """analyze_dataframe should preserve original columns."""
        result = vader_analyzer.analyze_dataframe(sample_df)
        
        assert 'review_text' in result.columns
        assert 'rating' in result.columns
        assert 'bank_name' in result.columns
    
    def test_analyze_dataframe_correct_length(self, vader_analyzer, sample_df):
        """analyze_dataframe should return same number of rows."""
        result = vader_analyzer.analyze_dataframe(sample_df)
        
        assert len(result) == len(sample_df)
    
    def test_analyze_dataframe_valid_labels(self, vader_analyzer, sample_df):
        """All labels should be POSITIVE, NEGATIVE, or NEUTRAL."""
        result = vader_analyzer.analyze_dataframe(sample_df)
        
        valid_labels = {'POSITIVE', 'NEGATIVE', 'NEUTRAL'}
        for label in result['sentiment_label_vader']:
            assert label in valid_labels
    
    def test_analyze_dataframe_scores_in_range(self, vader_analyzer, sample_df):
        """All scores should be between 0 and 1."""
        result = vader_analyzer.analyze_dataframe(sample_df)
        
        for score in result['sentiment_score_vader']:
            assert 0 <= score <= 1
    
    def test_analyze_dataframe_custom_column(self, vader_analyzer):
        """analyze_dataframe should work with custom text column."""
        df = pd.DataFrame({
            'text': ['Great!', 'Terrible!'],
            'other': [1, 2]
        })
        
        result = vader_analyzer.analyze_dataframe(df, text_column='text')
        
        assert 'sentiment_label_vader' in result.columns


class TestEdgeCases:
    """Tests for edge cases and special inputs."""
    
    @pytest.fixture
    def vader_analyzer(self):
        return SentimentAnalyzer(method='vader')
    
    def test_emoji_text(self, vader_analyzer):
        """Should handle emoji-only text."""
        result = vader_analyzer.analyze_text("😀😀😀")
        
        # VADER should recognize positive emojis
        assert result['label'] in ['POSITIVE', 'NEUTRAL']
    
    def test_numeric_text(self, vader_analyzer):
        """Should handle numeric text."""
        result = vader_analyzer.analyze_text("12345")
        
        assert result['label'] == 'NEUTRAL'
    
    def test_special_characters(self, vader_analyzer):
        """Should handle special characters."""
        result = vader_analyzer.analyze_text("!@#$%^&*()")
        
        # Should not crash
        assert result['label'] in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
    
    def test_very_long_text(self, vader_analyzer):
        """Should handle very long text."""
        long_text = "Great app! " * 1000  # ~11,000 characters
        result = vader_analyzer.analyze_text(long_text)
        
        assert result['label'] == 'POSITIVE'
    
    def test_non_english_text(self, vader_analyzer):
        """Should handle non-English text (may not be accurate)."""
        result = vader_analyzer.analyze_text("这个应用程序很好")  # Chinese
        
        # Should not crash, result may be neutral
        assert result['label'] in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
    
    def test_empty_dataframe(self, vader_analyzer):
        """Should handle empty DataFrame."""
        empty_df = pd.DataFrame({'review_text': []})
        result = vader_analyzer.analyze_dataframe(empty_df)
        
        assert len(result) == 0
        assert 'sentiment_label_vader' in result.columns
    
    def test_dataframe_with_nan(self, vader_analyzer):
        """Should handle DataFrame with NaN values."""
        df = pd.DataFrame({
            'review_text': ['Good', None, 'Bad', ''],
            'rating': [5, 4, 1, 2]
        })
        
        result = vader_analyzer.analyze_dataframe(df)
        
        # Should not crash and should have results for all rows
        assert len(result) == 4


class TestSentimentThresholds:
    """Tests for sentiment classification thresholds."""
    
    @pytest.fixture
    def vader_analyzer(self):
        return SentimentAnalyzer(method='vader')
    
    def test_threshold_boundary_positive(self, vader_analyzer):
        """Text at positive threshold boundary."""
        # Compound score around 0.05
        result = vader_analyzer.analyze_text("okay")
        
        # Should be classified based on compound score
        assert result['label'] in ['POSITIVE', 'NEUTRAL']
    
    def test_threshold_boundary_negative(self, vader_analyzer):
        """Text at negative threshold boundary."""
        # Compound score around -0.05
        result = vader_analyzer.analyze_text("not great")
        
        # Should be classified based on compound score
        assert result['label'] in ['NEGATIVE', 'NEUTRAL']


# Optional: DistilBERT tests (marked as slow)
@pytest.mark.slow
class TestDistilBertAnalyzer:
    """Tests for DistilBERT sentiment analysis.
    
    These tests are marked as slow because they require loading the model.
    Run with: pytest -m slow
    """
    
    @pytest.fixture(scope="class")
    def distilbert_analyzer(self):
        """Create DistilBERT analyzer (cached for class)."""
        return SentimentAnalyzer(method='distilbert')
    
    def test_init_distilbert(self, distilbert_analyzer):
        """Should initialize with DistilBERT method."""
        assert distilbert_analyzer.method == 'distilbert'
        assert distilbert_analyzer.model is not None
    
    def test_positive_text(self, distilbert_analyzer):
        """Positive text should return POSITIVE label."""
        result = distilbert_analyzer.analyze_text("This app is amazing!")
        
        assert result['label'] == 'POSITIVE'
    
    def test_negative_text(self, distilbert_analyzer):
        """Negative text should return NEGATIVE label."""
        result = distilbert_analyzer.analyze_text("This app is terrible!")
        
        assert result['label'] == 'NEGATIVE'
