#!/usr/bin/env python3
"""
Debug script to test data loading
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_processor import DataProcessor

def debug_data_loading():
    """Debug data loading issues"""
    print(f"Current working directory: {os.getcwd()}")
    
    # Test with default path
    processor = DataProcessor()
    print(f"Data path: '{processor.data_path}'")
    
    # Test individual file paths
    test_files = [
        "personal_finance_abhilasha.csv",
        "personal_finance_bukola.csv",
        "credit_card_customers.csv"
    ]
    
    for filename in test_files:
        full_path = f"{processor.data_path}{filename}"
        print(f"Testing path: '{full_path}'")
        print(f"File exists: {os.path.exists(full_path)}")
        
        if os.path.exists(full_path):
            try:
                import pandas as pd
                df = pd.read_csv(full_path)
                print(f"✅ {filename} loaded successfully - Shape: {df.shape}")
            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")
        else:
            print(f"❌ File not found: {full_path}")
        print("-" * 50)
    
    # Test load_datasets method
    print("\nTesting load_datasets method:")
    try:
        datasets = processor.load_datasets()
        print(f"Loaded {len(datasets)} datasets")
        for name, df in datasets.items():
            print(f"  {name}: {df.shape}")
    except Exception as e:
        print(f"Error in load_datasets: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_data_loading()
