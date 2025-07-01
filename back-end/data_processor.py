import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    """
    Handles data loading, cleaning, and preprocessing for the financial advisor system.
    """
    
    def __init__(self, data_path="data/raw_data/"):
        self.data_path = data_path
        self.label_encoders = {}
        self.scaler = StandardScaler()
        
    def load_datasets(self):
        """Load all available financial datasets"""
        datasets = {}
        
        try:
            # Load personal finance data
            datasets['personal_finance_1'] = pd.read_csv(f"{self.data_path}personal_finance_abhilasha.csv")
            datasets['personal_finance_2'] = pd.read_csv(f"{self.data_path}personal_finance_bukola.csv")
            
            # Load credit card data
            datasets['credit_customers'] = pd.read_csv(f"{self.data_path}credit_card_customers.csv")
            datasets['credit_data'] = pd.read_csv(f"{self.data_path}credit_card_data.csv")
            datasets['credit_defaults'] = pd.read_csv(f"{self.data_path}credit_card_defaults.csv")
            
            # Load financial habits data
            datasets['finance_habits'] = pd.read_csv(f"{self.data_path}indian_finance_habits.csv")
            
            # Load bank marketing data
            datasets['bank_marketing_1'] = pd.read_csv(f"{self.data_path}bank_marketing_henrique.csv", sep=';')
            datasets['bank_marketing_2'] = pd.read_csv(f"{self.data_path}bank_marketing_janiob.csv")
            datasets['bank_marketing_3'] = pd.read_csv(f"{self.data_path}bank_marketing_predictive.csv")
            
            print("Successfully loaded all datasets")
            return datasets
            
        except Exception as e:
            print(f"Error loading datasets: {e}")
            return {}
    
    def process_personal_finance_data(self, df):
        """Process personal finance transaction data"""
        if df.empty:
            return pd.DataFrame()
            
        try:
            # Clean and process the data
            date_columns = ['Date / Time', 'Date', 'date', 'DATE']
            date_col = None
            for col in date_columns:
                if col in df.columns:
                    date_col = col
                    break
            
            if date_col:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                df['Month'] = df[date_col].dt.month
                df['DayOfWeek'] = df[date_col].dt.dayofweek
            
            # Handle amount columns
            amount_columns = ['Debit/Credit', 'Amount', 'amount', 'AMOUNT']
            amount_col = None
            for col in amount_columns:
                if col in df.columns:
                    amount_col = col
                    break
            
            if amount_col:
                df['Amount'] = pd.to_numeric(df[amount_col], errors='coerce').fillna(0)
            else:
                df['Amount'] = 100  # Default amount if no amount column
            
            # Create spending categories
            if 'Category' in df.columns:
                df['Category_Clean'] = df['Category'].str.lower().str.strip()
            elif 'category' in df.columns:
                df['Category_Clean'] = df['category'].str.lower().str.strip()
            else:
                df['Category_Clean'] = 'general'
            
            # Handle Income/Expense column
            income_expense_cols = ['Income/Expense', 'Type', 'type', 'transaction_type']
            income_expense_col = None
            for col in income_expense_cols:
                if col in df.columns:
                    income_expense_col = col
                    break
            
            if income_expense_col:
                income_mask = df[income_expense_col].str.lower().str.contains('income', na=False)
                expense_mask = df[income_expense_col].str.lower().str.contains('expense', na=False)
            else:
                # Assume positive amounts are income, negative are expenses
                income_mask = df['Amount'] > 0
                expense_mask = df['Amount'] < 0
            
            # Aggregate by user behavior patterns
            user_stats = {
                'total_income': df[income_mask]['Amount'].sum(),
                'total_expense': df[expense_mask]['Amount'].sum(),
                'avg_transaction': df['Amount'].mean(),
                'transaction_count': len(df),
                'food_spending': df[df['Category_Clean'].str.contains('food', na=False)]['Amount'].sum(),
                'transport_spending': df[df['Category_Clean'].str.contains('transport', na=False)]['Amount'].sum(),
                'entertainment_spending': df[df['Category_Clean'].isin(['entertainment', 'other'])]['Amount'].sum()
            }
            
            return pd.DataFrame([user_stats])
            
        except Exception as e:
            print(f"Error processing personal finance data: {e}")
            # Return basic stats if processing fails
            return pd.DataFrame([{
                'total_income': 5000,
                'total_expense': 3000,
                'avg_transaction': 100,
                'transaction_count': 50,
                'food_spending': 800,
                'transport_spending': 200,
                'entertainment_spending': 300
            }])
    
    def process_credit_card_data(self, df):
        """Process credit card customer data"""
        if df.empty or 'Customer_Age' not in df.columns:
            return pd.DataFrame()
            
        # Select relevant features for financial profiling
        features = [
            'Customer_Age', 'Dependent_count', 'Credit_Limit', 
            'Total_Revolving_Bal', 'Avg_Open_To_Buy', 'Total_Trans_Amt',
            'Total_Trans_Ct', 'Avg_Utilization_Ratio'
        ]
        
        # Filter to existing features
        available_features = [f for f in features if f in df.columns]
        processed_df = df[available_features].copy()
        
        # Handle missing values
        processed_df = processed_df.fillna(processed_df.median())
        
        # Create financial behavior categories
        processed_df['high_utilization'] = (processed_df.get('Avg_Utilization_Ratio', 0) > 0.3).astype(int)
        processed_df['high_transaction_volume'] = (processed_df.get('Total_Trans_Ct', 0) > processed_df.get('Total_Trans_Ct', 0).median()).astype(int)
        
        return processed_df
    
    def process_finance_habits_data(self, df):
        """Process Indian finance habits dataset"""
        if df.empty:
            return pd.DataFrame()
            
        # Select key financial indicators
        financial_features = [
            'Income', 'Age', 'Dependents', 'Rent', 'Loan_Repayment',
            'Insurance', 'Groceries', 'Transport', 'Eating_Out',
            'Entertainment', 'Utilities', 'Healthcare', 'Education',
            'Desired_Savings_Percentage', 'Disposable_Income'
        ]
        
        # Filter to available columns
        available_features = [f for f in financial_features if f in df.columns]
        processed_df = df[available_features].copy()
        
        # Create derived features
        if 'Income' in processed_df.columns and 'Disposable_Income' in processed_df.columns:
            processed_df['savings_rate'] = processed_df['Disposable_Income'] / processed_df['Income']
            processed_df['expense_ratio'] = 1 - processed_df['savings_rate']
        
        # Create age groups
        if 'Age' in processed_df.columns:
            processed_df['age_group'] = pd.cut(processed_df['Age'], 
                                             bins=[0, 25, 35, 45, 55, 100], 
                                             labels=['young', 'early_career', 'mid_career', 'late_career', 'senior'])
            # Convert categorical to string to avoid concat issues
            processed_df['age_group'] = processed_df['age_group'].astype(str)
        
        return processed_df
    
    def create_unified_dataset(self, datasets):
        """Create a unified dataset for analysis"""
        unified_features = []
        
        # Process each dataset
        for name, df in datasets.items():
            try:
                if name.startswith('personal_finance'):
                    processed = self.process_personal_finance_data(df)
                    if not processed.empty:
                        processed['data_source'] = name
                        unified_features.append(processed)
                        
                elif name == 'credit_customers':
                    processed = self.process_credit_card_data(df)
                    if not processed.empty:
                        # Sample to avoid memory issues
                        if len(processed) > 1000:
                            processed = processed.sample(1000, random_state=42)
                        processed['data_source'] = name
                        unified_features.append(processed)
                        
                elif name == 'finance_habits':
                    processed = self.process_finance_habits_data(df)
                    if not processed.empty:
                        # Sample to avoid memory issues
                        if len(processed) > 1000:
                            processed = processed.sample(1000, random_state=42)
                        processed['data_source'] = name
                        unified_features.append(processed)
                        
            except Exception as e:
                print(f"Error processing dataset {name}: {e}")
                continue
        
        if unified_features:
            try:
                # Convert any categorical columns to strings before concatenation
                for df in unified_features:
                    categorical_cols = df.select_dtypes(include=['category']).columns
                    for col in categorical_cols:
                        df[col] = df[col].astype(str)
                
                # Combine all processed datasets
                unified_df = pd.concat(unified_features, ignore_index=True, sort=False)
                
                # Fill missing values with 0 for now (can be improved)
                unified_df = unified_df.fillna(0)
                
                return unified_df
            except Exception as e:
                print(f"Error combining datasets: {e}")
                return pd.DataFrame()
        else:
            print("No datasets could be processed successfully")
            return pd.DataFrame()
    
    def encode_categorical_features(self, df):
        """Encode categorical features using LabelEncoder"""
        categorical_columns = df.select_dtypes(include=['object']).columns
        
        for col in categorical_columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
            else:
                df[col] = self.label_encoders[col].transform(df[col].astype(str))
        
        return df
    
    def scale_features(self, df, fit=True):
        """Scale numerical features using StandardScaler"""
        numerical_columns = df.select_dtypes(include=[np.number]).columns
        
        if fit:
            df[numerical_columns] = self.scaler.fit_transform(df[numerical_columns])
        else:
            df[numerical_columns] = self.scaler.transform(df[numerical_columns])
        
        return df
    
    def prepare_data_for_modeling(self, datasets):
        """Complete data preparation pipeline"""
        print("Creating unified dataset...")
        unified_df = self.create_unified_dataset(datasets)
        
        if unified_df.empty:
            print("No data available for processing")
            return pd.DataFrame()
        
        print(f"Unified dataset shape: {unified_df.shape}")
        
        # Encode categorical features
        print("Encoding categorical features...")
        unified_df = self.encode_categorical_features(unified_df)
        
        # Scale features
        print("Scaling features...")
        unified_df = self.scale_features(unified_df)
        
        return unified_df
