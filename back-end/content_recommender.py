import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

class ContentBasedRecommender:
    """
    Implements content-based filtering for personalized financial recommendations.
    """
    
    def __init__(self):
        self.financial_products = None
        self.user_profiles = None
        self.similarity_matrix = None
        self.tfidf_vectorizer = TfidfVectorizer()
        
    def create_financial_products_database(self):
        """Create a comprehensive database of financial products and advice"""
        financial_products = {
            'savings_accounts': [
                {
                    'id': 'savings_001',
                    'name': 'High-Yield Savings Account',
                    'category': 'savings',
                    'risk_level': 'low',
                    'expected_return': 2.5,
                    'liquidity': 'high',
                    'min_investment': 100,
                    'target_age_group': 'all',
                    'target_income': 'low_to_medium',
                    'description': 'Safe savings option with competitive interest rates',
                    'features': ['FDIC insured', 'no monthly fees', 'online access'],
                    'suitable_for': ['emergency fund', 'short term goals', 'conservative investors']
                },
                {
                    'id': 'savings_002',
                    'name': 'Money Market Account',
                    'category': 'savings',
                    'risk_level': 'low',
                    'expected_return': 3.0,
                    'liquidity': 'medium',
                    'min_investment': 1000,
                    'target_age_group': 'all',
                    'target_income': 'medium_to_high',
                    'description': 'Higher yield savings with limited transactions',
                    'features': ['higher interest rates', 'check writing', 'FDIC insured'],
                    'suitable_for': ['emergency fund', 'medium term savings']
                }
            ],
            'investment_products': [
                {
                    'id': 'invest_001',
                    'name': 'Index Fund Portfolio',
                    'category': 'investment',
                    'risk_level': 'medium',
                    'expected_return': 7.0,
                    'liquidity': 'medium',
                    'min_investment': 1000,
                    'target_age_group': 'young_to_middle',
                    'target_income': 'medium_to_high',
                    'description': 'Diversified portfolio tracking market indices',
                    'features': ['low fees', 'automatic diversification', 'long-term growth'],
                    'suitable_for': ['retirement planning', 'long term wealth building']
                },
                {
                    'id': 'invest_002',
                    'name': 'Conservative Bond Fund',
                    'category': 'investment',
                    'risk_level': 'low',
                    'expected_return': 4.5,
                    'liquidity': 'medium',
                    'min_investment': 500,
                    'target_age_group': 'middle_to_senior',
                    'target_income': 'all',
                    'description': 'Stable income through government and corporate bonds',
                    'features': ['stable income', 'capital preservation', 'moderate risk'],
                    'suitable_for': ['income generation', 'capital preservation', 'retirement']
                },
                {
                    'id': 'invest_003',
                    'name': 'Growth Stock ETF',
                    'category': 'investment',
                    'risk_level': 'high',
                    'expected_return': 10.0,
                    'liquidity': 'high',
                    'min_investment': 100,
                    'target_age_group': 'young',
                    'target_income': 'medium_to_high',
                    'description': 'High-growth potential stocks for aggressive investors',
                    'features': ['high growth potential', 'liquid', 'higher volatility'],
                    'suitable_for': ['wealth building', 'long term growth', 'young investors']
                }
            ],
            'credit_products': [
                {
                    'id': 'credit_001',
                    'name': 'Cashback Credit Card',
                    'category': 'credit',
                    'risk_level': 'medium',
                    'expected_return': 2.0,  # cashback percentage
                    'liquidity': 'high',
                    'min_investment': 0,
                    'target_age_group': 'all',
                    'target_income': 'medium_to_high',
                    'description': 'Earn cashback on everyday purchases',
                    'features': ['cashback rewards', 'fraud protection', 'credit building'],
                    'suitable_for': ['daily expenses', 'reward earning', 'credit building']
                },
                {
                    'id': 'credit_002',
                    'name': 'Low-Interest Personal Loan',
                    'category': 'credit',
                    'risk_level': 'medium',
                    'expected_return': -5.5,  # negative because it's a cost
                    'liquidity': 'high',
                    'min_investment': 1000,
                    'target_age_group': 'all',
                    'target_income': 'medium_to_high',
                    'description': 'Consolidate debt or fund major purchases',
                    'features': ['fixed rates', 'predictable payments', 'debt consolidation'],
                    'suitable_for': ['debt consolidation', 'major purchases', 'home improvement']
                }
            ],
            'insurance_products': [
                {
                    'id': 'insurance_001',
                    'name': 'Term Life Insurance',
                    'category': 'insurance',
                    'risk_level': 'low',
                    'expected_return': 0.0,  # protection, not investment
                    'liquidity': 'low',
                    'min_investment': 200,  # annual premium
                    'target_age_group': 'young_to_middle',
                    'target_income': 'all',
                    'description': 'Affordable life insurance protection',
                    'features': ['affordable premiums', 'death benefit', 'term coverage'],
                    'suitable_for': ['family protection', 'mortgage protection', 'income replacement']
                },
                {
                    'id': 'insurance_002',
                    'name': 'Disability Insurance',
                    'category': 'insurance',
                    'risk_level': 'low',
                    'expected_return': 0.0,
                    'liquidity': 'low',
                    'min_investment': 300,
                    'target_age_group': 'young_to_middle',
                    'target_income': 'medium_to_high',
                    'description': 'Income protection in case of disability',
                    'features': ['income replacement', 'own occupation coverage', 'cost of living adjustments'],
                    'suitable_for': ['income protection', 'career protection', 'financial security']
                }
            ]
        }
        
        # Flatten the products into a single list
        all_products = []
        for category, products in financial_products.items():
            all_products.extend(products)
        
        self.financial_products = pd.DataFrame(all_products)
        return self.financial_products
    
    def create_budgeting_strategies(self):
        """Create personalized budgeting strategies"""
        budgeting_strategies = [
            {
                'id': 'budget_001',
                'name': '50/30/20 Rule',
                'category': 'budgeting',
                'description': 'Allocate 50% needs, 30% wants, 20% savings',
                'suitable_for': ['beginners', 'stable income', 'simple approach'],
                'income_level': 'medium_to_high',
                'complexity': 'low',
                'focus': 'balanced'
            },
            {
                'id': 'budget_002',
                'name': 'Zero-Based Budgeting',
                'category': 'budgeting',
                'description': 'Every dollar has a purpose, income minus expenses equals zero',
                'suitable_for': ['detailed planners', 'variable income', 'debt payoff'],
                'income_level': 'all',
                'complexity': 'high',
                'focus': 'control'
            },
            {
                'id': 'budget_003',
                'name': 'Envelope Method',
                'category': 'budgeting',
                'description': 'Cash-based budgeting for specific spending categories',
                'suitable_for': ['overspenders', 'cash users', 'visual learners'],
                'income_level': 'low_to_medium',
                'complexity': 'medium',
                'focus': 'spending_control'
            },
            {
                'id': 'budget_004',
                'name': 'Pay Yourself First',
                'category': 'budgeting',
                'description': 'Prioritize savings before any other expenses',
                'suitable_for': ['goal-oriented', 'disciplined savers', 'automation lovers'],
                'income_level': 'medium_to_high',
                'complexity': 'low',
                'focus': 'savings'
            }
        ]
        
        return pd.DataFrame(budgeting_strategies)
    
    def create_user_feature_vector(self, user_profile):
        """Create a feature vector for a user based on their financial profile"""
        features = {}
        
        # Basic demographics
        features['age'] = user_profile.get('age', 30)
        features['income'] = user_profile.get('income', 50000)
        features['dependents'] = user_profile.get('dependents', 0)
        
        # Financial behavior
        features['risk_tolerance'] = user_profile.get('risk_tolerance', 'medium')
        features['investment_experience'] = user_profile.get('investment_experience', 'beginner')
        features['savings_rate'] = user_profile.get('savings_rate', 0.1)
        features['debt_to_income'] = user_profile.get('debt_to_income', 0.3)
        
        # Goals and preferences
        features['primary_goal'] = user_profile.get('primary_goal', 'general_savings')
        features['time_horizon'] = user_profile.get('time_horizon', 'medium_term')
        features['liquidity_needs'] = user_profile.get('liquidity_needs', 'medium')
        
        return features
    
    def calculate_product_suitability(self, user_features, product):
        """Calculate how suitable a financial product is for a user"""
        suitability_score = 0.0
        
        # Age matching
        user_age = user_features.get('age', 30)
        target_age = product.get('target_age_group', 'all')
        
        if target_age == 'all':
            age_score = 1.0
        elif target_age == 'young' and user_age < 35:
            age_score = 1.0
        elif target_age == 'young_to_middle' and 25 <= user_age < 50:
            age_score = 1.0
        elif target_age == 'middle_to_senior' and user_age >= 40:
            age_score = 1.0
        else:
            age_score = 0.5
        
        # Income matching
        user_income = user_features.get('income', 50000)
        target_income = product.get('target_income', 'all')
        
        if target_income == 'all':
            income_score = 1.0
        elif target_income == 'low_to_medium' and user_income < 75000:
            income_score = 1.0
        elif target_income == 'medium_to_high' and user_income >= 40000:
            income_score = 1.0
        else:
            income_score = 0.5
        
        # Risk tolerance matching
        user_risk = user_features.get('risk_tolerance', 'medium')
        product_risk = product.get('risk_level', 'medium')
        
        risk_compatibility = {
            ('low', 'low'): 1.0,
            ('low', 'medium'): 0.7,
            ('low', 'high'): 0.3,
            ('medium', 'low'): 0.8,
            ('medium', 'medium'): 1.0,
            ('medium', 'high'): 0.8,
            ('high', 'low'): 0.5,
            ('high', 'medium'): 0.8,
            ('high', 'high'): 1.0
        }
        
        risk_score = risk_compatibility.get((user_risk, product_risk), 0.5)
        
        # Minimum investment check
        min_investment = product.get('min_investment', 0)
        user_available_funds = user_features.get('income', 50000) * user_features.get('savings_rate', 0.1)
        
        if min_investment <= user_available_funds:
            investment_score = 1.0
        elif min_investment <= user_available_funds * 2:
            investment_score = 0.7
        else:
            investment_score = 0.3
        
        # Calculate weighted suitability score
        suitability_score = (
            age_score * 0.2 +
            income_score * 0.25 +
            risk_score * 0.35 +
            investment_score * 0.2
        )
        
        return suitability_score
    
    def recommend_products(self, user_profile, n_recommendations=5):
        """Generate product recommendations for a user"""
        if self.financial_products is None:
            self.create_financial_products_database()
        
        user_features = self.create_user_feature_vector(user_profile)
        recommendations = []
        
        if self.financial_products is not None and not self.financial_products.empty:
            for _, product in self.financial_products.iterrows():
                suitability_score = self.calculate_product_suitability(user_features, product)
                
                recommendation = {
                    'product_id': product['id'],
                    'product_name': product['name'],
                    'category': product['category'],
                    'suitability_score': suitability_score,
                    'expected_return': product['expected_return'],
                    'risk_level': product['risk_level'],
                    'description': product['description'],
                    'features': product.get('features', []),
                    'suitable_for': product.get('suitable_for', [])
                }
                
                recommendations.append(recommendation)
            
            # Sort by suitability score
            recommendations.sort(key=lambda x: x['suitability_score'], reverse=True)
        
        return recommendations[:n_recommendations]
    
    def recommend_budgeting_strategy(self, user_profile):
        """Recommend budgeting strategies based on user profile"""
        budgeting_strategies = self.create_budgeting_strategies()
        user_features = self.create_user_feature_vector(user_profile)
        
        best_strategy = None
        best_score = 0
        
        for _, strategy in budgeting_strategies.iterrows():
            score = 0
            
            # Income level matching
            user_income = user_features.get('income', 50000)
            strategy_income = strategy.get('income_level', 'all')
            
            if strategy_income == 'all':
                score += 1
            elif strategy_income == 'low_to_medium' and user_income < 75000:
                score += 1
            elif strategy_income == 'medium_to_high' and user_income >= 40000:
                score += 1
            
            # User goals matching
            user_goal = user_features.get('primary_goal', 'general_savings')
            strategy_focus = strategy.get('focus', 'balanced')
            
            if user_goal in ['debt_payoff', 'emergency_fund'] and strategy_focus == 'control':
                score += 2
            elif user_goal in ['retirement', 'investment'] and strategy_focus == 'savings':
                score += 2
            elif strategy_focus == 'balanced':
                score += 1
            
            # Experience level
            complexity = strategy.get('complexity', 'medium')
            user_experience = user_features.get('investment_experience', 'beginner')
            
            if user_experience == 'beginner' and complexity == 'low':
                score += 1
            elif user_experience == 'intermediate' and complexity in ['low', 'medium']:
                score += 1
            elif user_experience == 'advanced':
                score += 1
            
            if score > best_score:
                best_score = score
                best_strategy = strategy
        
        if best_strategy is not None:
            return {
                'strategy_name': best_strategy['name'],
                'description': best_strategy['description'],
                'suitable_for': best_strategy['suitable_for'],
                'complexity': best_strategy['complexity'],
                'focus': best_strategy['focus'],
                'match_score': best_score
            }
        else:
            # Default strategy if no match found
            return {
                'strategy_name': '50/30/20 Rule',
                'description': 'Allocate 50% needs, 30% wants, 20% savings',
                'suitable_for': ['beginners', 'stable income', 'simple approach'],
                'complexity': 'low',
                'focus': 'balanced',
                'match_score': 0
            }
    
    def generate_personalized_advice(self, user_profile, cluster_info=None):
        """Generate comprehensive personalized financial advice"""
        advice = {}
        
        # Get product recommendations
        product_recommendations = self.recommend_products(user_profile)
        advice['product_recommendations'] = product_recommendations
        
        # Get budgeting strategy
        budgeting_strategy = self.recommend_budgeting_strategy(user_profile)
        advice['budgeting_strategy'] = budgeting_strategy
        
        # Generate general advice based on user profile
        user_features = self.create_user_feature_vector(user_profile)
        general_advice = []
        
        # Age-based advice
        age = user_features.get('age', 30)
        if age < 30:
            general_advice.append("Start investing early to take advantage of compound interest")
            general_advice.append("Focus on building an emergency fund of 3-6 months expenses")
        elif age < 50:
            general_advice.append("Maximize retirement contributions and consider tax-advantaged accounts")
            general_advice.append("Review and update your insurance coverage")
        else:
            general_advice.append("Consider more conservative investments as you approach retirement")
            general_advice.append("Plan for healthcare costs in retirement")
        
        # Savings rate advice
        savings_rate = user_features.get('savings_rate', 0.1)
        if savings_rate < 0.1:
            general_advice.append("Try to increase your savings rate to at least 10% of income")
        elif savings_rate > 0.2:
            general_advice.append("Excellent savings rate! Consider optimizing your investment allocation")
        
        # Debt advice
        debt_ratio = user_features.get('debt_to_income', 0.3)
        if debt_ratio > 0.4:
            general_advice.append("Focus on debt reduction using debt avalanche or snowball method")
        
        advice['general_advice'] = general_advice
        
        # Include cluster-based advice if available
        if cluster_info:
            advice['cluster_profile'] = cluster_info
            advice['peer_insights'] = self._generate_peer_insights(cluster_info)
        
        return advice
    
    def _generate_peer_insights(self, cluster_info):
        """Generate insights based on user's cluster/peer group"""
        insights = []
        
        profile_type = cluster_info.get('profile_type', 'Unknown')
        
        if 'Conservative' in profile_type:
            insights.append("Users with similar profiles typically prefer low-risk investments")
            insights.append("Consider diversifying with some medium-risk options for better returns")
        elif 'Spender' in profile_type:
            insights.append("Users in your group often benefit from automated savings")
            insights.append("Consider the envelope budgeting method to control spending")
        elif 'Saver' in profile_type:
            insights.append("Your peer group typically achieves above-average savings rates")
            insights.append("Consider increasing investment allocation for wealth building")
        
        return insights
    
    def save_recommender(self, filepath):
        """Save the recommender model"""
        recommender_data = {
            'financial_products': self.financial_products,
            'user_profiles': self.user_profiles
        }
        joblib.dump(recommender_data, filepath)
        print(f"Recommender saved to {filepath}")
    
    def load_recommender(self, filepath):
        """Load a saved recommender model"""
        recommender_data = joblib.load(filepath)
        self.financial_products = recommender_data['financial_products']
        self.user_profiles = recommender_data.get('user_profiles')
        print(f"Recommender loaded from {filepath}")
