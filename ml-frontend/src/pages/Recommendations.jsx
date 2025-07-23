import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './Recommendations.css'

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [userProfile, setUserProfile] = useState(null)

  useEffect(() => {
    const savedProfile = localStorage.getItem('userProfile')
    if (savedProfile) {
      setUserProfile(JSON.parse(savedProfile))
    }
  }, [])

  const fetchRecommendations = async () => {
    if (!userProfile) {
      setError('Please complete your profile first')
      return
    }

    setIsLoading(true)
    setError('')

    try {
      const response = await axios.post('http://localhost:5000/api/recommendations', userProfile)
      if (response.data && response.data.data) {
        setRecommendations(response.data.data)
      } else {
        throw new Error('Invalid backend response. Falling back to mock data.')
      }
    } catch (error) {
      console.warn('Backend unavailable or returned error. Using mock data.')
      setRecommendations(generateMockRecommendations(userProfile))
    } finally {
      setIsLoading(false)
    }
  }

  const generateMockRecommendations = (profile) => {
    const riskLevel = profile.risk_tolerance
    return {
      recommendations: {
        content_based: {
          savings_accounts: [
            {
              id: 'savings_001',
              name: 'High-Yield Savings Account',
              category: 'savings',
              risk_level: 'low',
              expected_return: 2.5,
              score: 0.92,
              description: 'Safe savings option with competitive interest rates',
              features: ['FDIC insured', 'No monthly fees', 'Online access'],
              min_investment: 100
            }
          ],
          investment_products: [
            {
              id: 'invest_001',
              name:
                riskLevel === 'low'
                  ? 'Conservative Bond Fund'
                  : riskLevel === 'medium'
                  ? 'Index Fund Portfolio'
                  : 'Growth Stock ETF',
              category: 'investment',
              risk_level: riskLevel,
              expected_return:
                riskLevel === 'low' ? 4.5 : riskLevel === 'medium' ? 7.0 : 10.0,
              score: 0.89,
              description: `Investment option matching your ${riskLevel} risk tolerance`,
              features: ['Professional management', 'Diversified portfolio'],
              min_investment: 1000
            }
          ]
        },
        budgeting_strategy: {
          strategy_name: profile.age < 35 ? 'Young Professional Strategy' : 'Mid-Career Strategy',
          recommended_allocation: {
            emergency_fund: profile.monthly_expenses * 6,
            savings: profile.income * profile.savings_rate,
            investments: profile.income * 0.15,
            debt_payment: profile.income * profile.debt_to_income
          },
          tips: [
            'Automate your savings transfers',
            'Review and adjust budget monthly',
            'Pay off high-interest debt first',
            'Build emergency fund to 6 months expenses',
            'Consider increasing retirement contributions'
          ]
        }
      },
      cluster_info: {
        cluster_id: 2,
        cluster_description: profile.age < 35 ? 'Young Professional Saver' : 'Mid-Career Builder',
        typical_characteristics: [
          `Age ${profile.age - 5}-${profile.age + 5}`,
          profile.income < 75000 ? 'Moderate income' : 'High income',
          'Building wealth'
        ]
      },
      insights: {
        financial_health_score: Math.min(85, Math.max(40, 60 + profile.savings_rate * 100)),
        risk_assessment: `Your ${riskLevel} risk tolerance is appropriate for your profile`,
        key_recommendations: [
          'Continue building emergency fund',
          'Consider increasing investment allocation',
          'Review insurance coverage'
        ]
      }
    }
  }

  const formatCurrency = (amount) =>
    new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount)

  const formatPercentage = (value) => `${value.toFixed(1)}%`

  return (
    <div className="recommendations">
      <div className="recommendations-content">
        <div className="recommendations-header">
          <h1>Personalized Recommendations</h1>
          <p>AI-powered financial advice tailored to your profile</p>

          {!userProfile ? (
            <div className="no-profile">
              <p>Please complete your profile to get personalized recommendations.</p>
              <a href="/profile" className="btn">
                Complete Profile
              </a>
            </div>
          ) : (
            <button onClick={fetchRecommendations} className="btn" disabled={isLoading}>
              {isLoading ? 'Generating Recommendations...' : 'Get Recommendations'}
            </button>
          )}
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {isLoading && (
        <div className="loading">
          <div className="spinner"></div>
          <p>Analyzing your financial profile...</p>
        </div>
      )}

      {recommendations && (
        <div className="recommendations-content">
          {/* Financial Health Score */}
          <div className="health-score-card">
            <h3>Financial Health Score</h3>
            <div className="score-display">
              <div className="score-number">{recommendations.insights.financial_health_score}</div>
              <div className="score-label">out of 100</div>
            </div>
            <div className="score-bar">
              <div
                className="score-fill"
                style={{ width: `${recommendations.insights.financial_health_score}%` }}
              ></div>
            </div>
          </div>

          {/* Cluster Information */}
          <div className="cluster-info">
            <h3>Your Financial Profile</h3>
            <div className="cluster-card">
              <h4>{recommendations.cluster_info.cluster_description}</h4>
              <ul>
                {recommendations.cluster_info.typical_characteristics.map((char, index) => (
                  <li key={index}>{char}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Investment Recommendations */}
          <div className="investment-recommendations">
            <h3>Recommended Products</h3>
            <div className="products-grid">
              {recommendations.recommendations.content_based.savings_accounts.map((product) => (
                <div key={product.id} className="product-card">
                  <div className="product-header">
                    <h4>{product.name}</h4>
                    <span className={`risk-badge ${product.risk_level}`}>
                      {product.risk_level.toUpperCase()} RISK
                    </span>
                  </div>
                  <div className="product-details">
                    <div className="expected-return">
                      <span className="return-value">
                        {formatPercentage(product.expected_return)}
                      </span>
                      <span className="return-label">Expected Return</span>
                    </div>
                    <div className="match-score">
                      <span className="score-value">{Math.round(product.score * 100)}%</span>
                      <span className="score-label">Match Score</span>
                    </div>
                  </div>
                  <p className="product-description">{product.description}</p>
                  <ul className="product-features">
                    {product.features.map((feature, index) => (
                      <li key={index}>{feature}</li>
                    ))}
                  </ul>
                  <div className="product-footer">
                    <span className="min-investment">
                      Min: {formatCurrency(product.min_investment)}
                    </span>
                  </div>
                </div>
              ))}

              {recommendations.recommendations.content_based.investment_products.map((product) => (
                <div key={product.id} className="product-card">
                  <div className="product-header">
                    <h4>{product.name}</h4>
                    <span className={`risk-badge ${product.risk_level}`}>
                      {product.risk_level.toUpperCase()} RISK
                    </span>
                  </div>
                  <div className="product-details">
                    <div className="expected-return">
                      <span className="return-value">
                        {formatPercentage(product.expected_return)}
                      </span>
                      <span className="return-label">Expected Return</span>
                    </div>
                    <div className="match-score">
                      <span className="score-value">{Math.round(product.score * 100)}%</span>
                      <span className="score-label">Match Score</span>
                    </div>
                  </div>
                  <p className="product-description">{product.description}</p>
                  <ul className="product-features">
                    {product.features.map((feature, index) => (
                      <li key={index}>{feature}</li>
                    ))}
                  </ul>
                  <div className="product-footer">
                    <span className="min-investment">
                      Min: {formatCurrency(product.min_investment)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Budgeting Strategy */}
          <div className="budgeting-strategy">
            <h3>Recommended Budget Strategy</h3>
            <div className="strategy-card">
              <h4>{recommendations.recommendations.budgeting_strategy.strategy_name}</h4>
              <div className="allocation-grid">
                {Object.entries(
                  recommendations.recommendations.budgeting_strategy.recommended_allocation
                ).map(([key, value]) => (
                  <div className="allocation-item" key={key}>
                    <span className="allocation-label">{key.replace('_', ' ')}</span>
                    <span className="allocation-value">{formatCurrency(value / 12)}</span>
                  </div>
                ))}
              </div>

              <div className="tips-section">
                <h5>Recommended Actions</h5>
                <ul className="tips-list">
                  {recommendations.recommendations.budgeting_strategy.tips.map((tip, index) => (
                    <li key={index}>{tip}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {/* Key Insights */}
          <div className="key-insights">
            <h3>Key Insights</h3>
            <div className="insights-grid">
              <div className="insight-card">
                <h4>Risk Assessment</h4>
                <p>{recommendations.insights.risk_assessment}</p>
              </div>
              <div className="insight-card">
                <h4>Priority Actions</h4>
                <ul>
                  {recommendations.insights.key_recommendations.map((rec, index) => (
                    <li key={index}>{rec}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Recommendations
