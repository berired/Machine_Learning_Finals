import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './Dashboard.css'

const Dashboard = () => {
  const [userProfile, setUserProfile] = useState(null)
  const [systemStatus, setSystemStatus] = useState(null)
  const [recommendations, setRecommendations] = useState(null)
  const [advice, setAdvice] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    const savedProfile = localStorage.getItem('userProfile')
    if (savedProfile) {
      setUserProfile(JSON.parse(savedProfile))
    }

    checkSystemStatus()
    initializeBackend()
  }, [])

  const checkSystemStatus = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/status')
      setSystemStatus(response.data)
    } catch (error) {
      setSystemStatus({
        status: 'offline',
        message: 'Backend service is not available',
        backend_available: false
      })
    }
  }

  const initializeBackend = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/initialize')
      if (response.data.status === 'success') {
        console.log('Backend initialized')
        if (userProfile) {
          fetchPersonalizedAdvice(userProfile)
          fetchContentRecommendations(userProfile)
        }
      } else {
        console.warn('Backend initialization failed:', response.data.message)
      }
    } catch (error) {
      console.error('Error initializing backend:', error)
    }
  }

  const fetchPersonalizedAdvice = async (profile) => {
    setIsLoading(true)
    try {
      const response = await axios.post('http://localhost:5000/api/advice', {
        user_profile: profile,
        use_collaborative: true
      })
      if (response.data.status === 'success') {
        setAdvice(response.data.data)
      } else {
        console.warn('Failed to get advice:', response.data.message)
      }
    } catch (error) {
      console.error('Error fetching advice:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const fetchContentRecommendations = async (profile) => {
    try {
      const response = await axios.post('http://localhost:5000/api/recommendations/content', {
        user_profile: profile
      })
      if (response.data.status === 'success') {
        setRecommendations(response.data.data)
      } else {
        console.warn('Failed to get recommendations:', response.data.message)
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error)
    }
  }

  const calculateFinancialMetrics = (profile) => {
    if (!profile) return null

    const monthlyIncome = profile.income / 12
    const monthlySavings = monthlyIncome * profile.savings_rate
    const monthlyDebtPayment = monthlyIncome * profile.debt_to_income
    const disposableIncome = monthlyIncome - profile.monthly_expenses - monthlyDebtPayment
    const emergencyFundTarget = profile.monthly_expenses * 6
    const savingsRate = profile.savings_rate * 100

    return {
      monthlyIncome,
      monthlySavings,
      monthlyDebtPayment,
      disposableIncome,
      emergencyFundTarget,
      savingsRate,
      debtToIncomeRatio: profile.debt_to_income * 100
    }
  }

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount)
  }

  const formatPercentage = (value) => {
    return `${value.toFixed(1)}%`
  }

  const getFinancialHealthColor = (score) => {
    if (score >= 80) return 'excellent'
    if (score >= 70) return 'good'
    if (score >= 60) return 'fair'
    return 'poor'
  }

  const metrics = userProfile ? calculateFinancialMetrics(userProfile) : null

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Financial Dashboard</h1>
        <p>Overview of your financial health and system status</p>
      </div>

      {/* System Status */}
      <div className="status-section">
        <h2>System Status</h2>
        <div className={`status-card ${systemStatus?.status || 'offline'}`}>
          <div className="status-indicator">
            <div className={`status-dot ${systemStatus?.status || 'offline'}`}></div>
            <span className="status-text">
              {systemStatus?.status === 'running' ? 'AI System Online' : 'AI System Offline'}
            </span>
          </div>
          <p className="status-message">
            {systemStatus?.message || 'Checking system status...'}
          </p>
          {systemStatus?.backend_available === false && (
            <div className="fallback-notice">
              <p>⚠️ Using fallback mode with mock data</p>
            </div>
          )}
        </div>
      </div>

      {/* Profile Overview */}
      {userProfile ? (
        <div className="profile-overview">
          <h2>Profile Overview</h2>
          <div className="overview-grid">
            <div className="overview-card">
              <h4>Basic Info</h4>
              <div className="info-grid">
                <div className="info-item">
                  <span className="info-label">Age</span>
                  <span className="info-value">{userProfile.age} years</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Risk Tolerance</span>
                  <span className={`info-value risk-${userProfile.risk_tolerance}`}>
                    {userProfile.risk_tolerance.toUpperCase()}
                  </span>
                </div>
                <div className="info-item">
                  <span className="info-label">Experience</span>
                  <span className="info-value">{userProfile.investment_experience}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Primary Goal</span>
                  <span className="info-value">{userProfile.financial_goals.replace('_', ' ')}</span>
                </div>
              </div>
            </div>

            <div className="overview-card">
              <h4>Financial Health Score</h4>
              <div className="health-score-display">
                <div className="score-circle">
                  <div className={`score-number ${getFinancialHealthColor(60 + (userProfile.savings_rate * 100))}`}>
                    {Math.round(60 + (userProfile.savings_rate * 100))}
                  </div>
                  <div className="score-label">out of 100</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="no-profile-dashboard">
          <h2>No Profile Found</h2>
          <p>Complete your financial profile to see personalized dashboard metrics.</p>
          <a href="/profile" className="btn">Create Profile</a>
        </div>
      )}

      {/* Financial Metrics */}
      {metrics && (
        <div className="financial-metrics">
          <h2>Financial Metrics</h2>
          <div className="metrics-grid">
            <div className="metric-card income">
              <div className="metric-header">
                <h4>Monthly Income</h4>
                <span className="metric-icon">💰</span>
              </div>
              <div className="metric-value">{formatCurrency(metrics.monthlyIncome)}</div>
              <div className="metric-subtext">Before taxes and deductions</div>
            </div>

            <div className="metric-card expenses">
              <div className="metric-header">
                <h4>Monthly Expenses</h4>
                <span className="metric-icon">💳</span>
              </div>
              <div className="metric-value">{formatCurrency(userProfile.monthly_expenses)}</div>
              <div className="metric-subtext">
                {formatPercentage((userProfile.monthly_expenses / metrics.monthlyIncome) * 100)} of income
              </div>
            </div>

            <div className="metric-card savings">
              <div className="metric-header">
                <h4>Monthly Savings</h4>
                <span className="metric-icon">🏦</span>
              </div>
              <div className="metric-value">{formatCurrency(metrics.monthlySavings)}</div>
              <div className="metric-subtext">
                {formatPercentage(metrics.savingsRate)} savings rate
              </div>
            </div>

            <div className="metric-card debt">
              <div className="metric-header">
                <h4>Debt Payments</h4>
                <span className="metric-icon">📊</span>
              </div>
              <div className="metric-value">{formatCurrency(metrics.monthlyDebtPayment)}</div>
              <div className="metric-subtext">
                {formatPercentage(metrics.debtToIncomeRatio)} debt-to-income
              </div>
            </div>

            <div className="metric-card emergency">
              <div className="metric-header">
                <h4>Emergency Fund Target</h4>
                <span className="metric-icon">🛡️</span>
              </div>
              <div className="metric-value">{formatCurrency(metrics.emergencyFundTarget)}</div>
              <div className="metric-subtext">6 months of expenses</div>
            </div>

            <div className="metric-card disposable">
              <div className="metric-header">
                <h4>Disposable Income</h4>
                <span className="metric-icon">💸</span>
              </div>
              <div className={`metric-value ${metrics.disposableIncome < 0 ? 'negative' : 'positive'}`}>
                {formatCurrency(Math.abs(metrics.disposableIncome))}
              </div>
              <div className="metric-subtext">
                {metrics.disposableIncome < 0 ? 'Budget deficit' : 'Available for investments'}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Personalized Advice Section */}
      {isLoading && <p>Loading personalized advice...</p>}
      {advice && (
        <div className="advice-section">
          <h2>Personalized Financial Advice</h2>
          <pre>{JSON.stringify(advice, null, 2)}</pre>
        </div>
      )}

      {/* Content Recommendations Section */}
      {recommendations && (
        <div className="recommendations-section">
          <h2>Content Recommendations</h2>
          <pre>{JSON.stringify(recommendations, null, 2)}</pre>
        </div>
      )}

      {/* Quick Actions */}
      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="actions-grid">
          <a href="/profile" className="action-card">
            <div className="action-icon">👤</div>
            <h4>Update Profile</h4>
            <p>Modify your financial information and preferences</p>
          </a>

          <a href="/recommendations" className="action-card">
            <div className="action-icon">🎯</div>
            <h4>Get Recommendations</h4>
            <p>Receive personalized financial advice from AI</p>
          </a>

          <div className="action-card" onClick={checkSystemStatus}>
            <div className="action-icon">🔄</div>
            <h4>Refresh Status</h4>
            <p>Check current system status and connectivity</p>
          </div>

          <div className="action-card">
            <div className="action-icon">📈</div>
            <h4>View Analytics</h4>
            <p>Detailed analysis of your financial trends</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
