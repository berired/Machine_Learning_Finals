from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sys
import os
import logging

# Add the current directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from financial_advisor import PersonalizedFinancialAdvisor
    BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import financial_advisor: {e}")
    BACKEND_AVAILABLE = False

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to store the financial advisor instance
financial_advisor = None

def initialize_financial_advisor():
    """Initialize the financial advisor system"""
    global financial_advisor
    if BACKEND_AVAILABLE and financial_advisor is None:
        try:
            financial_advisor = PersonalizedFinancialAdvisor()
            success = financial_advisor.initialize_system()
            if success:
                logger.info("Financial advisor system initialized successfully")
                return True
            else:
                logger.warning("Financial advisor system initialization returned False")
                return False
        except Exception as e:
            logger.error(f"Error initializing financial advisor: {e}")
            return False
    return financial_advisor is not None

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get the status of the financial advisor system"""
    return jsonify({
        'status': 'running',
        'backend_available': BACKEND_AVAILABLE,
        'initialized': financial_advisor is not None,
        'message': 'Financial Advisor API is running'
    })

@app.route('/api/initialize', methods=['POST'])
def initialize_system():
    """Initialize the financial advisor system"""
    try:
        success = initialize_financial_advisor()
        if success:
            return jsonify({
                'status': 'success',
                'message': 'System initialized successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to initialize system'
            }), 500
    except Exception as e:
        logger.error(f"Error in initialize_system: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/advice', methods=['POST'])
def get_personalized_advice():
    """Get personalized financial advice for a user"""
    try:
        data = request.get_json()
        if not data or 'user_profile' not in data:
            return jsonify({
                'status': 'error',
                'message': 'user_profile is required'
            }), 400

        user_profile = data['user_profile']
        use_collaborative = data.get('use_collaborative', True)

        # If backend is not available, return mock data
        if not BACKEND_AVAILABLE or financial_advisor is None:
            return jsonify(get_mock_advice(user_profile))

        # Get advice from the financial advisor
        advice = financial_advisor.get_personalized_advice(
            user_profile, 
            use_collaborative=use_collaborative
        )
        
        return jsonify({
            'status': 'success',
            'data': advice
        })

    except Exception as e:
        logger.error(f"Error in get_personalized_advice: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/recommendations/content', methods=['POST'])
def get_content_recommendations():
    """Get content-based recommendations"""
    try:
        data = request.get_json()
        if not data or 'user_profile' not in data:
            return jsonify({
                'status': 'error',
                'message': 'user_profile is required'
            }), 400

        user_profile = data['user_profile']

        if not BACKEND_AVAILABLE or financial_advisor is None:
            return jsonify({
                'status': 'success',
                'data': get_mock_content_recommendations(user_profile)
            })

        # Get content recommendations
        recommendations = financial_advisor.content_recommender.recommend_products(user_profile)
        
        return jsonify({
            'status': 'success',
            'data': recommendations
        })

    except Exception as e:
        logger.error(f"Error in get_content_recommendations: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/budgeting', methods=['POST'])
def get_budgeting_strategy():
    """Get budgeting strategy recommendations"""
    try:
        data = request.get_json()
        if not data or 'user_profile' not in data:
            return jsonify({
                'status': 'error',
                'message': 'user_profile is required'
            }), 400

        user_profile = data['user_profile']

        if not BACKEND_AVAILABLE or financial_advisor is None:
            return jsonify({
                'status': 'success',
                'data': get_mock_budgeting_strategy(user_profile)
            })

        # Get budgeting strategy
        strategy = financial_advisor.content_recommender.recommend_budgeting_strategy(user_profile)
        
        return jsonify({
            'status': 'success',
            'data': strategy
        })

    except Exception as e:
        logger.error(f"Error in get_budgeting_strategy: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/profile', methods=['POST'])
def save_user_profile():
    """Save user profile"""
    try:
        profile = request.get_json()
        if not profile:
            return jsonify({
                'status': 'error',
                'message': 'Profile data is required'
            }), 400

        # In a real application, you would save this to a database
        # For now, we'll just return success
        profile_id = f"user_{hash(str(profile)) % 10000}"
        
        return jsonify({
            'status': 'success',
            'profile_id': profile_id,
            'message': 'Profile saved successfully'
        })

    except Exception as e:
        logger.error(f"Error in save_user_profile: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def get_mock_advice(user_profile):
    """Generate mock advice when backend is not available"""
    risk_level = user_profile.get('risk_tolerance', 'medium')
    age = user_profile.get('age', 30)
    income = user_profile.get('income', 50000)
    
    return {
        'status': 'success',
        'data': {
            'user_profile': user_profile,
            'timestamp': '2025-06-30T00:00:00Z',
            'recommendations': {
                'content_based': get_mock_content_recommendations(user_profile),
                'budgeting_strategy': get_mock_budgeting_strategy(user_profile)
            },
            'cluster_info': {
                'cluster_id': 2,
                'cluster_description': 'Young Professional Saver' if age < 35 else 'Mid-Career Builder',
                'typical_characteristics': [
                    f'Age {age-5}-{age+5}',
                    'Moderate income' if income < 75000 else 'High income',
                    'Building wealth'
                ]
            },
            'insights': {
                'financial_health_score': min(85, max(40, 60 + (user_profile.get('savings_rate', 0.1) * 100))),
                'risk_assessment': f"Your {risk_level} risk tolerance is appropriate for your profile",
                'key_recommendations': [
                    'Continue building emergency fund',
                    'Consider increasing investment allocation',
                    'Review insurance coverage'
                ]
            }
        }
    }

def get_mock_content_recommendations(user_profile):
    """Generate mock content recommendations"""
    risk_level = user_profile.get('risk_tolerance', 'medium')
    
    return {
        'savings_accounts': [
            {
                'id': 'savings_001',
                'name': 'High-Yield Savings Account',
                'category': 'savings',
                'risk_level': 'low',
                'expected_return': 2.5,
                'score': 0.92,
                'description': 'Safe savings option with competitive interest rates',
                'features': ['FDIC insured', 'no monthly fees', 'online access'],
                'min_investment': 100
            }
        ],
        'investment_products': [
            {
                'id': 'invest_001',
                'name': 'Conservative Bond Fund' if risk_level == 'low' else 
                       'Index Fund Portfolio' if risk_level == 'medium' else 'Growth Stock ETF',
                'category': 'investment',
                'risk_level': risk_level,
                'expected_return': 4.5 if risk_level == 'low' else 7.0 if risk_level == 'medium' else 10.0,
                'score': 0.89,
                'description': f'Investment option matching your {risk_level} risk tolerance',
                'features': ['Professional management', 'Diversified portfolio'],
                'min_investment': 1000
            }
        ]
    }

def get_mock_budgeting_strategy(user_profile):
    """Generate mock budgeting strategy"""
    age = user_profile.get('age', 30)
    income = user_profile.get('income', 50000)
    monthly_expenses = user_profile.get('monthly_expenses', 3000)
    savings_rate = user_profile.get('savings_rate', 0.1)
    
    return {
        'strategy_name': 'Young Professional Strategy' if age < 35 else 'Mid-Career Strategy',
        'recommended_allocation': {
            'emergency_fund': monthly_expenses * 6,
            'savings': income * savings_rate,
            'investments': income * 0.15,
            'debt_payment': income * user_profile.get('debt_to_income', 0.3)
        },
        'tips': [
            'Automate your savings transfers',
            'Review and adjust budget monthly',
            'Pay off high-interest debt first',
            'Build emergency fund to 6 months expenses',
            'Consider increasing retirement contributions'
        ],
        'budget_breakdown': {
            'housing': 0.28,
            'transportation': 0.15,
            'food': 0.12,
            'utilities': 0.08,
            'savings': savings_rate,
            'other': 0.37 - savings_rate
        }
    }

if __name__ == '__main__':
    # Initialize the system on startup
    initialize_financial_advisor()
    
    # Run the Flask app
    app.run(debug=True, port=5000, host='0.0.0.0')
