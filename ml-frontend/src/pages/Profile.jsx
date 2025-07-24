import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './Profile.css'

const Profile = () => {
  const [formData, setFormData] = useState({
    age: '',
    income: '',
    monthly_expenses: '',
    savings_rate: '',
    debt_to_income: '',
    risk_tolerance: 'medium',
    investment_experience: 'beginner',
    financial_goals: 'retirement'
  })
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState('')

  useEffect(() => {
    const savedProfile = localStorage.getItem('userProfile')
    if (savedProfile) {
      setFormData(JSON.parse(savedProfile))
    }
  }, [])

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setMessage('')

    try {
      const profileData = {
        ...formData,
        age: parseInt(formData.age),
        income: parseFloat(formData.income),
        monthly_expenses: parseFloat(formData.monthly_expenses),
        savings_rate: parseFloat(formData.savings_rate) / 100,
        debt_to_income: parseFloat(formData.debt_to_income) / 100
      }

      localStorage.setItem('userProfile', JSON.stringify(profileData))

      try {
        const response = await axios.post('http://localhost:5000/api/profile', profileData)
        setMessage('Profile saved successfully!')
        setMessageType('success')
      } catch (error) {
        console.error('Backend not available or error:', error)
        setMessage('Profile saved locally. Backend connection not available.')
        setMessageType('warning')
      }
    } catch (error) {
      setMessage('Error saving profile. Please try again.')
      setMessageType('error')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="profile">
      <div className="profile-header">
        <h1>Financial Profile</h1>
        <p>Help us understand your financial situation to provide personalized recommendations</p>
      </div>

      <form onSubmit={handleSubmit} className="profile-form">
        <div className="form-section">
          <h3>Personal Information</h3>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="age">Age</label>
              <input
                type="number"
                id="age"
                name="age"
                value={formData.age}
                onChange={handleInputChange}
                min="18"
                max="100"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="income">Annual Income ($)</label>
              <input
                type="number"
                id="income"
                name="income"
                value={formData.income}
                onChange={handleInputChange}
                min="0"
                step="1000"
                required
              />
            </div>
            <div className="form-group"></div>
          </div>
        </div>

        <div className="form-section">
          <h3>Financial Details</h3>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="monthly_expenses">Monthly Expenses ($)</label>
              <input
                type="number"
                id="monthly_expenses"
                name="monthly_expenses"
                value={formData.monthly_expenses}
                onChange={handleInputChange}
                min="0"
                step="100"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="savings_rate">Savings Rate (%)</label>
              <input
                type="number"
                id="savings_rate"
                name="savings_rate"
                value={formData.savings_rate}
                onChange={handleInputChange}
                min="0"
                max="100"
                step="1"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="debt_to_income">Debt to Income Ratio (%)</label>
              <input
                type="number"
                id="debt_to_income"
                name="debt_to_income"
                value={formData.debt_to_income}
                onChange={handleInputChange}
                min="0"
                max="100"
                step="1"
                required
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>Investment Preferences</h3>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="risk_tolerance">Risk Tolerance</label>
              <select
                id="risk_tolerance"
                name="risk_tolerance"
                value={formData.risk_tolerance}
                onChange={handleInputChange}
                required
              >
                <option value="low">Low - Prefer safe investments</option>
                <option value="medium">Medium - Balanced approach</option>
                <option value="high">High - Willing to take risks for higher returns</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="investment_experience">Investment Experience</label>
              <select
                id="investment_experience"
                name="investment_experience"
                value={formData.investment_experience}
                onChange={handleInputChange}
                required
              >
                <option value="beginner">Beginner - Little to no experience</option>
                <option value="intermediate">Intermediate - Some experience</option>
                <option value="advanced">Advanced - Experienced investor</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="financial_goals">Primary Financial Goal</label>
              <select
                id="financial_goals"
                name="financial_goals"
                value={formData.financial_goals}
                onChange={handleInputChange}
                required
              >
                <option value="retirement">Retirement Planning</option>
                <option value="emergency_fund">Emergency Fund</option>
                <option value="house_purchase">House Purchase</option>
                <option value="debt_reduction">Debt Reduction</option>
                <option value="wealth_building">Wealth Building</option>
                <option value="education">Education Funding</option>
              </select>
            </div>
          </div>
        </div>

        {message && (
          <div className={`message ${messageType}`}>
            {message}
          </div>
        )}

        <div className="form-actions">
          <button type="submit" className="btn" disabled={isLoading}>
            {isLoading ? (
              <>
                <span className="spinner"></span>
                Saving Profile...
              </>
            ) : (
              'Save Profile'
            )}
          </button>
        </div>
      </form>
    </div>
  )
}

export default Profile
