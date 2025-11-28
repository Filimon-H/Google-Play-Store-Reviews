"""Quick test for sentiment analyzer"""
import sys
sys.path.insert(0, 'src')

from sentiment_analyzer import SentimentAnalyzer

print("=" * 60)
print("TESTING VADER SENTIMENT ANALYZER")
print("=" * 60)

# Initialize VADER
analyzer = SentimentAnalyzer('vader')

# Test cases
test_reviews = [
    ("This app is amazing! I love it so much.", "Expected: POSITIVE"),
    ("Terrible app, crashes all the time. Waste of time.", "Expected: NEGATIVE"),
    ("The app works okay.", "Expected: NEUTRAL"),
    ("Fast transfers but UI needs improvement", "Expected: MIXED"),
    ("Login never works!!! Worst banking app ever 😡", "Expected: NEGATIVE"),
]

print("\nTest Results:")
print("-" * 60)
for text, expected in test_reviews:
    result = analyzer.analyze_text(text)
    print(f"\nText: \"{text[:50]}...\"")
    print(f"  {expected}")
    print(f"  Got: {result['label']} (score: {result['score']:.3f})")

print("\n" + "=" * 60)
print("VADER test complete!")
print("=" * 60)
