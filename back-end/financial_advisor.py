import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import our custom modules
from data_processor import DataProcessor
from user_profiler import UserProfiler
from content_recommender import ContentBasedRecommender
from collaborative_recommender import CollaborativeFilteringRecommender

class PersonalizedFinancialAdvisor:
    """
    Main class that integrates all components to provide personalized financial advice.
    """
    
    def __init__(self, data_path="data/raw_data/"):
        self.data_path = data_path
        self.data_processor = DataProcessor(data_path)
        self.user_profiler = UserProfiler()
        self.content_recommender = ContentBasedRecommender()
        self.collaborative_recommender = CollaborativeFilteringRecommender()
        
        # Data storage
        self.raw_datasets = {}
        self.processed_data = None
        self.user_clusters = None
        self.cluster_analysis = None
        
    def initialize_system(self):
        """Initialize the financial advisor system by loading and processing data"""
        print("=== Initializing Personalized Financial Advisor ===")
        
        # Load datasets
        print("1. Loading datasets...")
        self.raw_datasets = self.data_processor.load_datasets()
        
        if not self.raw_datasets:
            print("Warning: No datasets loaded. System will use default recommendations.")
            return False
        
        # Process data
        print("2. Processing and unifying data...")
        self.processed_data = self.data_processor.prepare_data_for_modeling(self.raw_datasets)
        
        if self.processed_data.empty:
            print("Warning: No processed data available. Using basic recommendations.")
            return False
        
        # Create user clusters
        print("3. Creating user profiles and clusters...")
        self.user_clusters = self.user_profiler.create_user_clusters(self.processed_data)
        
        if self.user_clusters is not None:
            self.cluster_analysis = self.user_profiler.analyze_clusters(self.user_clusters)
            print(f"Created {self.user_profiler.n_clusters} user clusters")
        
        # Initialize content-based recommender
        print("4. Setting up content-based recommendations...")
        self.content_recommender.create_financial_products_database()
        
        # Set up collaborative filtering if enough data
        if self.user_clusters is not None and len(self.user_clusters) > 10:
            print("5. Training collaborative filtering...")
            self._setup_collaborative_filtering()
        else:
            print("5. Skipping collaborative filtering (insufficient data)")
        
        print("✅ System initialization complete!")
        return True
    
    def _setup_collaborative_filtering(self):
        """Set up collaborative filtering with synthetic interaction data"""
        try:
            # Generate user profiles from cluster data
            user_profiles = []
            product_recommendations = []
            
            if self.user_clusters is not None:
                for _, user_row in self.user_clusters.iterrows():
                    # Create user profile from cluster data
                    user_profile = {
                        'age': user_row.get('Customer_Age', user_row.get('Age', 35)),
                        'income': user_row.get('Income', user_row.get('Credit_Limit', 50000)),
                        'dependents': user_row.get('Dependent_count', user_row.get('Dependents', 0)),
                        'risk_tolerance': 'medium',
                        'savings_rate': user_row.get('savings_rate', 0.1),
                        'debt_to_income': 0.3
                    }
                    user_profiles.append(user_profile)
                    
                    # Get content recommendations for this user
                    recommendations = self.content_recommender.recommend_products(user_profile)
                    product_recommendations.append(recommendations)
            else:
                print("Warning: user_clusters is None, skipping collaborative filtering setup.")
                return
            
            # Create interaction data
            interactions_df = self.collaborative_recommender.create_user_product_interactions(
                user_profiles, product_recommendations
            )
            
            # Train collaborative model
            if not interactions_df.empty:
                self.collaborative_recommender.train_collaborative_model(interactions_df)
                print("Collaborative filtering model trained successfully")
            
        except Exception as e:
            print(f"Error setting up collaborative filtering: {e}")
    
    def get_personalized_advice(self, user_profile, use_collaborative=True):
        """
        Generate comprehensive personalized financial advice for a user.
        
        Args:
            user_profile (dict): User's financial profile
            use_collaborative (bool): Whether to use collaborative filtering
            
        Returns:
            dict: Comprehensive financial advice
        """
        advice = {
            'user_profile': user_profile,
            'timestamp': datetime.now().isoformat(),
            'recommendations': {},
            'insights': {},
            'cluster_info': None
        }
        
        try:
            # 1. Predict user cluster
            if self.user_clusters is not None:
                cluster_info = self._get_user_cluster_info(user_profile)
                advice['cluster_info'] = cluster_info
            
            # 2. Get content-based recommendations
            content_recommendations = self.content_recommender.recommend_products(user_profile)
            advice['recommendations']['content_based'] = content_recommendations
            
            # 3. Get budgeting strategy
            budgeting_strategy = self.content_recommender.recommend_budgeting_strategy(user_profile)
            advice['recommendations']['budgeting_strategy'] = budgeting_strategy
            
            # 4. Get collaborative recommendations if available
            if use_collaborative and hasattr(self.collaborative_recommender, 'user_product_matrix'):
                if self.collaborative_recommender.user_product_matrix is not None:
                    # For new users, use cold start approach
                    collaborative_recs = self.collaborative_recommender.cold_start_recommendation(
                        user_profile, [user_profile], self.content_recommender
                    )
                    advice['recommendations']['collaborative'] = collaborative_recs
                    
                    # Generate hybrid recommendations
                    hybrid_recs = self.collaborative_recommender.hybrid_recommendation(
                        0, content_recommendations  # Use user_id 0 for new users
                    )
                    advice['recommendations']['hybrid'] = hybrid_recs
            
            # 5. Generate comprehensive advice
            comprehensive_advice = self.content_recommender.generate_personalized_advice(
                user_profile, advice['cluster_info']
            )
            advice['recommendations'].update(comprehensive_advice)
            
            # 6. Generate insights
            advice['insights'] = self._generate_insights(user_profile, advice)
            
        except Exception as e:
            print(f"Error generating advice: {e}")
            # Provide basic recommendations as fallback
            advice['recommendations']['content_based'] = self.content_recommender.recommend_products(user_profile)
            advice['recommendations']['budgeting_strategy'] = self.content_recommender.recommend_budgeting_strategy(user_profile)
        
        return advice
    
    def _get_user_cluster_info(self, user_profile):
        """Get cluster information for a user"""
        try:
            if self.user_profiler.kmeans is None:
                return None
            
            # Get the actual feature names from the training data
            if self.processed_data is None or self.processed_data.empty:
                return None
                
            # Create a feature vector with the same structure as training data
            # Initialize with zeros
            user_features = pd.DataFrame(0, index=[0], columns=self.processed_data.columns)
            
            # Map user profile values to training data columns
            user_age = user_profile.get('age', 35)
            user_income = user_profile.get('income', 50000)
            user_dependents = user_profile.get('dependents', 0)
            user_savings_rate = user_profile.get('savings_rate', 0.1)
            user_debt_ratio = user_profile.get('debt_to_income', 0.3)
            
            # Map to available columns in training data
            if 'Age' in user_features.columns:
                user_features['Age'] = user_age
            if 'Customer_Age' in user_features.columns:
                user_features['Customer_Age'] = user_age
                
            if 'Income' in user_features.columns:
                user_features['Income'] = user_income
            if 'Credit_Limit' in user_features.columns:
                user_features['Credit_Limit'] = user_income * 0.3  # Estimate credit limit
                
            if 'Dependents' in user_features.columns:
                user_features['Dependents'] = user_dependents
            if 'Dependent_count' in user_features.columns:
                user_features['Dependent_count'] = user_dependents
                
            if 'savings_rate' in user_features.columns:
                user_features['savings_rate'] = user_savings_rate
            if 'Desired_Savings_Percentage' in user_features.columns:
                user_features['Desired_Savings_Percentage'] = user_savings_rate * 100
                
            # Set some reasonable defaults for other financial features
            if 'total_income' in user_features.columns:
                user_features['total_income'] = user_income
            if 'total_expense' in user_features.columns:
                user_features['total_expense'] = user_income * (1 - user_savings_rate)
            if 'avg_transaction' in user_features.columns:
                user_features['avg_transaction'] = 150
            if 'transaction_count' in user_features.columns:
                user_features['transaction_count'] = 20
                
            # Predict cluster
            cluster_id = self.user_profiler.predict_user_cluster(user_features)
            
            # Get cluster interpretation
            if self.cluster_analysis and f'cluster_{cluster_id}' in self.cluster_analysis:
                cluster_info = self.cluster_analysis[f'cluster_{cluster_id}']
                cluster_interpretations = self.user_profiler.interpret_clusters(self.cluster_analysis)
                
                return {
                    'cluster_id': cluster_id,
                    'profile_type': cluster_interpretations[f'cluster_{cluster_id}']['profile_type'],
                    'characteristics': cluster_interpretations[f'cluster_{cluster_id}']['characteristics'],
                    'cluster_size': cluster_info.get('size', 0),
                    'cluster_percentage': cluster_info.get('percentage', 0)
                }
            
        except Exception as e:
            print(f"Error getting cluster info: {e}")
        
        return None
    
    def _generate_insights(self, user_profile, advice):
        """Generate actionable insights based on user profile and recommendations"""
        insights = {
            'financial_health_score': 0,
            'key_recommendations': [],
            'risk_assessment': {},
            'goal_analysis': {},
            'priority_actions': []
        }
        
        try:
            # Calculate financial health score
            insights['financial_health_score'] = self._calculate_financial_health_score(user_profile)
            
            # Risk assessment
            insights['risk_assessment'] = self._assess_financial_risk(user_profile)
            
            # Goal analysis
            insights['goal_analysis'] = self._analyze_financial_goals(user_profile)
            
            # Priority actions
            insights['priority_actions'] = self._generate_priority_actions(user_profile, insights)
            
            # Key recommendations based on cluster
            if advice.get('cluster_info'):
                insights['key_recommendations'] = self._get_cluster_based_recommendations(
                    advice['cluster_info']
                )
            
        except Exception as e:
            print(f"Error generating insights: {e}")
        
        return insights
    
    def _calculate_financial_health_score(self, user_profile):
        """Calculate a financial health score (0-100)"""
        score = 50  # Base score
        
        # Savings rate
        savings_rate = user_profile.get('savings_rate', 0.1)
        if savings_rate >= 0.2:
            score += 20
        elif savings_rate >= 0.1:
            score += 10
        elif savings_rate < 0.05:
            score -= 10
        
        # Debt to income ratio
        debt_ratio = user_profile.get('debt_to_income', 0.3)
        if debt_ratio <= 0.2:
            score += 15
        elif debt_ratio <= 0.3:
            score += 5
        elif debt_ratio > 0.5:
            score -= 20
        
        # Emergency fund (estimated)
        emergency_fund_months = user_profile.get('emergency_fund_months', 3)
        if emergency_fund_months >= 6:
            score += 15
        elif emergency_fund_months >= 3:
            score += 5
        else:
            score -= 10
        
        return max(0, min(100, score))
    
    def _assess_financial_risk(self, user_profile):
        """Assess financial risks"""
        risks = []
        
        if user_profile.get('debt_to_income', 0.3) > 0.4:
            risks.append("High debt-to-income ratio")
        
        if user_profile.get('savings_rate', 0.1) < 0.05:
            risks.append("Low savings rate")
        
        if user_profile.get('emergency_fund_months', 3) < 3:
            risks.append("Insufficient emergency fund")
        
        age = user_profile.get('age', 35)
        if age > 50 and user_profile.get('retirement_savings', 0) < user_profile.get('income', 50000):
            risks.append("Inadequate retirement savings")
        
        return {
            'risk_level': 'high' if len(risks) >= 3 else 'medium' if len(risks) >= 1 else 'low',
            'identified_risks': risks
        }
    
    def _analyze_financial_goals(self, user_profile):
        """Analyze user's financial goals"""
        primary_goal = user_profile.get('primary_goal', 'general_savings')
        time_horizon = user_profile.get('time_horizon', 'medium_term')
        
        goal_analysis = {
            'primary_goal': primary_goal,
            'time_horizon': time_horizon,
            'feasibility': 'medium',
            'recommended_approach': []
        }
        
        if primary_goal == 'retirement':
            goal_analysis['recommended_approach'] = [
                'Maximize employer 401(k) match',
                'Consider tax-advantaged accounts',
                'Focus on long-term growth investments'
            ]
        elif primary_goal == 'emergency_fund':
            goal_analysis['recommended_approach'] = [
                'Start with high-yield savings account',
                'Automate savings',
                'Target 3-6 months of expenses'
            ]
        elif primary_goal == 'debt_payoff':
            goal_analysis['recommended_approach'] = [
                'Use debt avalanche or snowball method',
                'Consider debt consolidation',
                'Avoid new debt while paying off existing'
            ]
        
        return goal_analysis
    
    def _generate_priority_actions(self, user_profile, insights):
        """Generate priority actions based on analysis"""
        actions = []
        
        # Based on financial health score
        health_score = insights.get('financial_health_score', 50)
        if health_score < 40:
            actions.append("Focus on debt reduction and emergency fund building")
        elif health_score < 70:
            actions.append("Optimize savings rate and investment allocation")
        else:
            actions.append("Consider advanced investment strategies and tax optimization")
        
        # Based on risks
        risks = insights.get('risk_assessment', {}).get('identified_risks', [])
        for risk in risks[:2]:  # Top 2 risks
            if "debt" in risk.lower():
                actions.append("Create a debt reduction plan")
            elif "savings" in risk.lower():
                actions.append("Increase automatic savings")
            elif "emergency" in risk.lower():
                actions.append("Build emergency fund to 3-6 months expenses")
        
        return actions[:3]  # Return top 3 priority actions
    
    def _get_cluster_based_recommendations(self, cluster_info):
        """Get recommendations based on user's cluster"""
        recommendations = []
        
        profile_type = cluster_info.get('profile_type', '')
        
        if 'Conservative' in profile_type:
            recommendations.extend([
                "Consider adding some growth investments for better returns",
                "Explore tax-advantaged savings accounts",
                "Review insurance coverage for complete protection"
            ])
        elif 'Spender' in profile_type:
            recommendations.extend([
                "Implement automated savings to build wealth",
                "Use budgeting apps to track expenses",
                "Consider the 24-hour rule before major purchases"
            ])
        elif 'Saver' in profile_type:
            recommendations.extend([
                "Optimize investment allocation for growth",
                "Consider real estate or alternative investments",
                "Review and rebalance portfolio regularly"
            ])
        
        return recommendations[:3]
    
    def visualize_user_profile(self, user_profile, advice, save_path=None):
        """Create visualizations for user's financial profile"""
        try:
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('Personal Financial Analysis Dashboard', fontsize=16, fontweight='bold')
            
            # 1. Financial Health Score
            ax1 = axes[0, 0]
            health_score = advice['insights'].get('financial_health_score', 50)
            colors = ['red' if health_score < 40 else 'orange' if health_score < 70 else 'green']
            ax1.bar(['Financial Health'], [health_score], color=colors[0], alpha=0.7)
            ax1.set_ylim(0, 100)
            ax1.set_ylabel('Score')
            ax1.set_title('Financial Health Score')
            ax1.text(0, health_score + 2, f'{health_score:.0f}', ha='center', fontweight='bold')
            
            # 2. Risk Assessment
            ax2 = axes[0, 1]
            risk_info = advice['insights'].get('risk_assessment', {})
            risk_level = risk_info.get('risk_level', 'medium')
            risk_counts = {'low': 0, 'medium': 0, 'high': 0}
            risk_counts[risk_level] = 1
            
            colors_risk = ['green', 'orange', 'red']
            ax2.pie(list(risk_counts.values()), labels=['Low Risk', 'Medium Risk', 'High Risk'], 
                   colors=colors_risk, autopct='%1.0f%%', startangle=90)
            ax2.set_title('Risk Assessment')
            
            # 3. Recommendation Categories
            ax3 = axes[1, 0]
            content_recs = advice['recommendations'].get('content_based', [])
            categories = {}
            for rec in content_recs:
                cat = rec.get('category', 'other')
                categories[cat] = categories.get(cat, 0) + 1
            
            if categories:
                ax3.bar(categories.keys(), categories.values(), alpha=0.7)
                ax3.set_title('Recommended Product Categories')
                ax3.set_ylabel('Number of Recommendations')
                plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
            
            # 4. User Profile Summary
            ax4 = axes[1, 1]
            profile_data = [
                user_profile.get('age', 35),
                user_profile.get('income', 50000) / 1000,  # in thousands
                user_profile.get('savings_rate', 0.1) * 100,  # as percentage
                user_profile.get('debt_to_income', 0.3) * 100  # as percentage
            ]
            profile_labels = ['Age', 'Income (K)', 'Savings Rate (%)', 'Debt Ratio (%)']
            
            ax4.barh(profile_labels, profile_data, alpha=0.7)
            ax4.set_title('User Profile Overview')
            ax4.set_xlabel('Values')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            else:
                plt.savefig('user_financial_profile.png', dpi=300, bbox_inches='tight')
            
            plt.show()
            
        except Exception as e:
            print(f"Error creating visualizations: {e}")
    
    def generate_report(self, user_profile, advice):
        """Generate a comprehensive financial report"""
        report = {
            'executive_summary': {},
            'detailed_analysis': {},
            'recommendations': {},
            'action_plan': {}
        }
        
        try:
            # Executive Summary
            health_score = advice['insights'].get('financial_health_score', 50)
            risk_level = advice['insights'].get('risk_assessment', {}).get('risk_level', 'medium')
            
            report['executive_summary'] = {
                'financial_health_score': health_score,
                'risk_level': risk_level,
                'cluster_profile': advice.get('cluster_info', {}).get('profile_type', 'Unknown') if advice.get('cluster_info') else 'Unknown',
                'top_priority': advice['insights'].get('priority_actions', ['Review financial plan'])[0] if advice['insights'].get('priority_actions') else 'Review financial plan'
            }
            
            # Detailed Analysis
            report['detailed_analysis'] = {
                'user_profile': user_profile,
                'cluster_analysis': advice.get('cluster_info'),
                'risk_assessment': advice['insights'].get('risk_assessment'),
                'goal_analysis': advice['insights'].get('goal_analysis')
            }
            
            # Recommendations
            report['recommendations'] = advice['recommendations']
            
            # Action Plan
            report['action_plan'] = {
                'immediate_actions': advice['insights'].get('priority_actions', [])[:2],
                'short_term_goals': ['Review and update budget', 'Increase emergency fund'],
                'long_term_strategy': ['Diversify investments', 'Plan for retirement']
            }
            
        except Exception as e:
            print(f"Error generating report: {e}")
        
        return report
    
    def save_models(self, directory="models/"):
        """Save all trained models"""
        import os
        os.makedirs(directory, exist_ok=True)
        
        try:
            # Save user profiler
            if self.user_profiler.kmeans is not None:
                self.user_profiler.save_model(f"{directory}user_profiler.pkl")
            
            # Save content recommender
            self.content_recommender.save_recommender(f"{directory}content_recommender.pkl")
            
            # Save collaborative recommender
            if hasattr(self.collaborative_recommender, 'user_product_matrix'):
                if self.collaborative_recommender.user_product_matrix is not None:
                    self.collaborative_recommender.save_model(f"{directory}collaborative_recommender.pkl")
            
            # Save data processor
            joblib.dump(self.data_processor, f"{directory}data_processor.pkl")
            
            print(f"Models saved to {directory}")
            
        except Exception as e:
            print(f"Error saving models: {e}")
    
    def load_models(self, directory="models/"):
        """Load pre-trained models"""
        import os
        
        try:
            # Load user profiler
            if os.path.exists(f"{directory}user_profiler.pkl"):
                self.user_profiler.load_model(f"{directory}user_profiler.pkl")
            
            # Load content recommender
            if os.path.exists(f"{directory}content_recommender.pkl"):
                self.content_recommender.load_recommender(f"{directory}content_recommender.pkl")
            
            # Load collaborative recommender
            if os.path.exists(f"{directory}collaborative_recommender.pkl"):
                self.collaborative_recommender.load_model(f"{directory}collaborative_recommender.pkl")
            
            # Load data processor
            if os.path.exists(f"{directory}data_processor.pkl"):
                self.data_processor = joblib.load(f"{directory}data_processor.pkl")
            
            print(f"Models loaded from {directory}")
            
        except Exception as e:
            print(f"Error loading models: {e}")


# Example usage function
def create_sample_user_profile():
    """Create a sample user profile for testing"""
    return {
        'age': 32,
        'income': 75000,
        'dependents': 1,
        'risk_tolerance': 'medium',
        'investment_experience': 'beginner',
        'savings_rate': 0.15,
        'debt_to_income': 0.25,
        'primary_goal': 'retirement',
        'time_horizon': 'long_term',
        'liquidity_needs': 'medium',
        'emergency_fund_months': 4
    }


if __name__ == "__main__":
    # Example usage
    print("Personalized Financial Advisor System")
    print("=" * 50)
    
    # Initialize the system
    advisor = PersonalizedFinancialAdvisor()
    
    # Initialize with data
    success = advisor.initialize_system()
    
    if success:
        # Create a sample user profile
        user_profile = create_sample_user_profile()
        
        # Get personalized advice
        advice = advisor.get_personalized_advice(user_profile)
        
        # Generate visualizations
        advisor.visualize_user_profile(user_profile, advice)
        
        # Generate report
        report = advisor.generate_report(user_profile, advice)
        
        # Print summary
        print("\n=== FINANCIAL ADVICE SUMMARY ===")
        print(f"Financial Health Score: {advice['insights'].get('financial_health_score', 'N/A')}/100")
        print(f"Risk Level: {advice['insights'].get('risk_assessment', {}).get('risk_level', 'N/A')}")
        
        if advice.get('cluster_info'):
            print(f"User Profile Type: {advice['cluster_info'].get('profile_type', 'N/A')}")
        
        print("\nTop Priority Actions:")
        for action in advice['insights'].get('priority_actions', [])[:3]:
            print(f"• {action}")
        
        print("\nTop Product Recommendations:")
        content_recs = advice['recommendations'].get('content_based', [])
        for i, rec in enumerate(content_recs[:3], 1):
            print(f"{i}. {rec.get('product_name', 'N/A')} (Score: {rec.get('suitability_score', 0):.2f})")
        
        print(f"\nRecommended Budgeting Strategy: {advice['recommendations'].get('budgeting_strategy', {}).get('strategy_name', 'N/A')}")
        
        # Save models
        advisor.save_models()
        
    else:
        print("System initialization failed. Please check your data files.")
