  import React from 'react'
  import { Link } from 'react-router-dom'
  import './Home.css'

  const Home = () => {
    return (
      <div className="home">
        <section className="hero">
          <div className="hero-content">
            <h1 className="hero-title">
              Your Personal <span className="text-accent">Financial</span> AI Advisor
            </h1>
            <p className="hero-subtitle">
              Get personalized financial recommendations powered by machine learning. 
              Make smarter decisions about savings, investments, and budgeting.
            </p>
            <div className="hero-actions">
              <Link to="/profile" className="btn">
                Get Started
              </Link>
              <Link to="/dashboard" className="btn btn-secondary">
                View Dashboard
              </Link>
            </div>
          </div>
          <div className="hero-visual">
            <div className="financial-cards">
              <div className="floating-card">
                <div className="card-header">
                  <h4>Savings Goal</h4>
                </div>
                <div className="progress-bar">
                  <div className="progress-fill" style={{width: '75%'}}></div>
                </div>
                <p className="text-accent">$7,500 / $10,000</p>
              </div>
              
              <div className="floating-card">
                <div className="card-header">
                  <h4>Investment Portfolio</h4>
                </div>
                <div className="metric">
                  <span className="metric-value text-accent">+12.5%</span>
                  <span className="metric-label">This Year</span>
                </div>
              </div>
              
              <div className="floating-card">
                <div className="card-header">
                  <h4>Monthly Budget</h4>
                </div>
                <div className="budget-breakdown">
                  <div className="budget-item">
                    <span>Spent</span>
                    <span className="text-accent">$2,340</span>
                  </div>
                  <div className="budget-item">
                    <span>Remaining</span>
                    <span className="text-secondary">$660</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="features">
          <div className="section-header">
            <h2>Why Choose FinAdvisor AI?</h2>
            <p>Advanced machine learning algorithms analyze your financial patterns to provide personalized recommendations</p>
          </div>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>Personalized Recommendations</h3>
              <p>Get tailored financial advice based on your unique profile, goals, and risk tolerance.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Smart Analytics</h3>
              <p>Advanced data analysis provides insights into your spending patterns and financial health.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>AI-Powered Insights</h3>
              <p>Machine learning algorithms continuously learn from your behavior to improve recommendations.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🔒</div>
              <h3>Secure & Private</h3>
              <p>Your financial data is encrypted and protected with bank-level security measures.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📱</div>
              <h3>Responsive Design</h3>
              <p>Access your financial dashboard from any device with our mobile-friendly interface.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Real-time Updates</h3>
              <p>Get instant notifications and updates on your financial goals and market changes.</p>
            </div>
          </div>
        </section>

        <section className="cta">
          <div className="cta-content">
            <h2>Ready to Transform Your Financial Future?</h2>
            <p>Join thousands of users who have improved their financial health with AI-powered insights.</p>
            <Link to="/profile" className="btn">
              Create Your Profile
            </Link>
          </div>
        </section>
      </div>
    )
  }

  export default Home
