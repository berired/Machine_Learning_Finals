#!/usr/bin/env python3
"""
Test script for the Personalized Financial Advisor System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from financial_advisor import PersonalizedFinancialAdvisor, create_sample_user_profile

def test_financial_advisor():
    """Test the financial advisor system"""
    print("🧪 Testing Personalized Financial Advisor System")
    print("=" * 60)
    
    # Initialize the system
    advisor = PersonalizedFinancialAdvisor()
    
    # Test initialization
    print("1. Testing system initialization...")
    success = advisor.initialize_system()
    
    if not success:
        print("❌ System initialization failed")
        return False
    
    print("✅ System initialized successfully")
    
    # Test with different user profiles
    test_profiles = [
        {
            'name': 'Young Professional',
            'profile': {
                'age': 28,
                'income': 60000,
                'dependents': 0,
                'risk_tolerance': 'high',
                'savings_rate': 0.20,
                'debt_to_income': 0.15,
                'primary_goal': 'emergency_fund',
                'time_horizon': 'short_term'
            }
        },
        {
            'name': 'Family Person',
            'profile': {
                'age': 35,
                'income': 85000,
                'dependents': 2,
                'risk_tolerance': 'medium',
                'savings_rate': 0.12,
                'debt_to_income': 0.35,
                'primary_goal': 'retirement',
                'time_horizon': 'long_term'
            }
        },
        {
            'name': 'Near Retirement',
            'profile': {
                'age': 58,
                'income': 95000,
                'dependents': 0,
                'risk_tolerance': 'low',
                'savings_rate': 0.25,
                'debt_to_income': 0.10,
                'primary_goal': 'retirement',
                'time_horizon': 'short_term'
            }
        }
    ]
    
    print("\n2. Testing advice generation for different user profiles...")
    
    for test_case in test_profiles:
        print(f"\n--- Testing: {test_case['name']} ---")
        
        try:
            # Get personalized advice
            advice = advisor.get_personalized_advice(test_case['profile'])
            
            # Verify advice structure
            assert 'user_profile' in advice, "Missing user_profile in advice"
            assert 'recommendations' in advice, "Missing recommendations in advice"
            assert 'insights' in advice, "Missing insights in advice"
            
            # Check financial health score
            health_score = advice['insights'].get('financial_health_score', 0)
            print(f"   Financial Health Score: {health_score}/100")
            
            # Check cluster info
            cluster_info = advice.get('cluster_info')
            if cluster_info:
                print(f"   Profile Type: {cluster_info.get('profile_type', 'Unknown')}")
                print(f"   Cluster ID: {cluster_info.get('cluster_id', 'Unknown')}")
            
            # Check recommendations
            content_recs = advice['recommendations'].get('content_based', [])
            print(f"   Recommendations: {len(content_recs)} products")
            
            # Check budgeting strategy
            budget_strategy = advice['recommendations'].get('budgeting_strategy', {})
            print(f"   Budgeting Strategy: {budget_strategy.get('strategy_name', 'N/A')}")
            
            # Generate report
            report = advisor.generate_report(test_case['profile'], advice)
            assert 'executive_summary' in report, "Missing executive_summary in report"
            
            print(f"   ✅ {test_case['name']} test passed")
            
        except Exception as e:
            print(f"   ❌ {test_case['name']} test failed: {e}")
            return False
    
    print("\n3. Testing model persistence...")
    try:
        # Test saving models
        advisor.save_models("test_models/")
        print("   ✅ Models saved successfully")
        
        # Test loading models
        new_advisor = PersonalizedFinancialAdvisor()
        new_advisor.load_models("test_models/")
        print("   ✅ Models loaded successfully")
        
        # Clean up test models
        import shutil
        shutil.rmtree("test_models/", ignore_errors=True)
        
    except Exception as e:
        print(f"   ❌ Model persistence test failed: {e}")
        return False
    
    print("\n🎉 All tests passed! The system is working correctly.")
    return True

if __name__ == "__main__":
    success = test_financial_advisor()
    exit(0 if success else 1)
