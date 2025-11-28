"""
Export data from PostgreSQL to CSV for dashboard deployment.
Run this once to create the CSV file for Streamlit Cloud.
"""
import sys
sys.path.insert(0, 'src')

from database import DatabaseManager
import pandas as pd

def export_data():
    print("Connecting to database...")
    db = DatabaseManager()
    db.connect()
    
    query = """
        SELECT r.*, b.bank_name, b.bank_code
        FROM reviews r
        JOIN banks b ON r.bank_id = b.bank_id;
    """
    
    print("Fetching data...")
    with db.engine.connect() as conn:
        df = pd.read_sql(query, conn)
    
    # Save to dashboard/data folder
    output_path = 'dashboard/data/reviews_final.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Exported {len(df):,} reviews to {output_path}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nBanks: {df['bank_name'].unique().tolist()}")
    
    db.disconnect()

if __name__ == "__main__":
    export_data()
