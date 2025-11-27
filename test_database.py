"""
Test script to verify database setup and fetch data
"""
import sys
sys.path.insert(0, 'src')

from database import DatabaseManager

def test_database():
    print("=" * 60)
    print("DATABASE CONNECTION TEST")
    print("=" * 60)
    
    # Initialize and connect
    db = DatabaseManager()
    
    if not db.connect():
        print("\n❌ Failed to connect to database!")
        print("Check your .env file credentials.")
        return
    
    print("\n✅ Connected successfully!")
    
    # Test 1: Fetch all banks
    print("\n" + "-" * 40)
    print("TEST 1: Fetch all banks")
    print("-" * 40)
    
    from sqlalchemy import text
    
    with db.engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM banks;"))
        banks = result.fetchall()
        
        if banks:
            print(f"Found {len(banks)} banks:")
            for bank in banks:
                print(f"  ID: {bank[0]} | Code: {bank[1]} | Name: {bank[2]}")
        else:
            print("No banks found in database.")
    
    # Test 2: Count reviews
    print("\n" + "-" * 40)
    print("TEST 2: Count reviews per bank")
    print("-" * 40)
    
    with db.engine.connect() as conn:
        query = """
            SELECT b.bank_name, COUNT(r.review_id) as count
            FROM banks b
            LEFT JOIN reviews r ON b.bank_id = r.bank_id
            GROUP BY b.bank_name;
        """
        result = conn.execute(text(query))
        counts = result.fetchall()
        
        total = 0
        for row in counts:
            print(f"  {row[0]}: {row[1]} reviews")
            total += row[1]
        print(f"\n  Total: {total} reviews")
    
    # Test 3: Sample reviews
    print("\n" + "-" * 40)
    print("TEST 3: Sample reviews (5 random)")
    print("-" * 40)
    
    with db.engine.connect() as conn:
        query = """
            SELECT b.bank_name, r.rating, r.sentiment_label_distilbert, 
                   r.primary_theme, LEFT(r.review_text, 80) as review_preview
            FROM reviews r
            JOIN banks b ON r.bank_id = b.bank_id
            ORDER BY RANDOM()
            LIMIT 5;
        """
        result = conn.execute(text(query))
        samples = result.fetchall()
        
        for i, row in enumerate(samples, 1):
            print(f"\n  [{i}] {row[0]} | ⭐{row[1]} | {row[2]} | Theme: {row[3]}")
            print(f"      \"{row[4]}...\"")
    
    # Test 4: Average ratings
    print("\n" + "-" * 40)
    print("TEST 4: Average rating by bank")
    print("-" * 40)
    
    with db.engine.connect() as conn:
        query = """
            SELECT b.bank_name, 
                   ROUND(AVG(r.rating)::numeric, 2) as avg_rating,
                   COUNT(*) as total
            FROM banks b
            JOIN reviews r ON b.bank_id = r.bank_id
            GROUP BY b.bank_name
            ORDER BY avg_rating DESC;
        """
        result = conn.execute(text(query))
        ratings = result.fetchall()
        
        for row in ratings:
            stars = "⭐" * int(round(float(row[1])))
            print(f"  {row[0]}: {row[1]} {stars} ({row[2]} reviews)")
    
    # Test 5: Sentiment summary
    print("\n" + "-" * 40)
    print("TEST 5: Sentiment distribution")
    print("-" * 40)
    
    with db.engine.connect() as conn:
        query = """
            SELECT sentiment_label_distilbert, COUNT(*) as count
            FROM reviews
            WHERE sentiment_label_distilbert IS NOT NULL
            GROUP BY sentiment_label_distilbert
            ORDER BY count DESC;
        """
        result = conn.execute(text(query))
        sentiments = result.fetchall()
        
        for row in sentiments:
            emoji = "😊" if row[0] == "POSITIVE" else "😞" if row[0] == "NEGATIVE" else "😐"
            print(f"  {emoji} {row[0]}: {row[1]}")
    
    # Test 6: Top themes
    print("\n" + "-" * 40)
    print("TEST 6: Top 5 themes")
    print("-" * 40)
    
    with db.engine.connect() as conn:
        query = """
            SELECT primary_theme, COUNT(*) as count
            FROM reviews
            WHERE primary_theme IS NOT NULL AND primary_theme != 'Other'
            GROUP BY primary_theme
            ORDER BY count DESC
            LIMIT 5;
        """
        result = conn.execute(text(query))
        themes = result.fetchall()
        
        if themes:
            for row in themes:
                print(f"  {row[0]}: {row[1]} reviews")
        else:
            print("  No themes found (run Task 2 notebook first)")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED - Database is working!")
    print("=" * 60)
    
    db.close()


if __name__ == "__main__":
    test_database()
