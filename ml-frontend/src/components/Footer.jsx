import React, { useState } from 'react'
import './Footer.css'

const Footer = () => {
  const [email, setEmail] = useState('')
  const [isSubscribed, setIsSubscribed] = useState(false)

  const handleNewsletterSubmit = (e) => {
    e.preventDefault()
    if (email) {
      setIsSubscribed(true)
      setEmail('')
      setTimeout(() => setIsSubscribed(false), 3000)
    }
  }

  const socialLinks = [
    { name: 'Twitter', icon: '🐦', url: '#' },
    { name: 'LinkedIn', icon: '💼', url: '#' },
    { name: 'Facebook', icon: '📘', url: '#' },
    { name: 'Instagram', icon: '📸', url: '#' }
  ]

  const currentYear = new Date().getFullYear()

  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-main">
          <div className="footer-section footer-brand">
            <div className="brand-logo">
              <div className="logo-icon">💰</div>
              <h3>FinAdvisor AI</h3>
            </div>
            <p className="brand-description">
              Empowering your financial future with intelligent AI-driven insights and personalized recommendations.
            </p>
            <div className="social-links">
              {socialLinks.map((social, index) => (
                <a
                  key={index}
                  href={social.url}
                  className="social-link"
                  aria-label={social.name}
                  title={social.name}
                >
                  <span className="social-icon">{social.icon}</span>
                </a>
              ))}
            </div>
          </div>

          <div className="footer-section">
            <h4>Platform</h4>
            <ul className="footer-links">
              <li><a href="#dashboard">Dashboard</a></li>
              <li><a href="#profile">Profile Setup</a></li>
              <li><a href="#recommendations">AI Recommendations</a></li>
              <li><a href="#analytics">Analytics</a></li>
              <li><a href="#goals">Financial Goals</a></li>
              <li><a href="#budgeting">Budget Tracker</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Resources</h4>
            <ul className="footer-links">
              <li><a href="#blog">Financial Blog</a></li>
              <li><a href="#guides">Investment Guides</a></li>
              <li><a href="#calculators">Financial Calculators</a></li>
              <li><a href="#webinars">Webinars</a></li>
              <li><a href="#api">API Documentation</a></li>
              <li><a href="#faq">FAQ</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Company</h4>
            <ul className="footer-links">
              <li><a href="#about">About Us</a></li>
              <li><a href="#careers">Careers</a></li>
              <li><a href="#press">Press Kit</a></li>
              <li><a href="#contact">Contact</a></li>
              <li><a href="#partners">Partners</a></li>
              <li><a href="#investors">Investors</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Support</h4>
            <ul className="footer-links">
              <li><a href="#help">Help Center</a></li>
              <li><a href="#support">Customer Support</a></li>
              <li><a href="#security">Security</a></li>
              <li><a href="#status">System Status</a></li>
              <li><a href="#feedback">Feedback</a></li>
              <li><a href="#community">Community</a></li>
            </ul>
          </div>

          <div className="footer-section newsletter-section">
            <h4>Stay Updated</h4>
            <p>Get weekly financial tips and market insights delivered to your inbox.</p>
            <div className="newsletter-form">
              <div className="input-group">
                <input
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="newsletter-input"
                  onKeyPress={(e) => e.key === 'Enter' && handleNewsletterSubmit(e)}
                />
                <button onClick={handleNewsletterSubmit} className="newsletter-btn">
                  {isSubscribed ? '✓' : 'Subscribe'}
                </button>
              </div>
              {isSubscribed && (
                <p className="success-message">Thanks for subscribing!</p>
              )}
            </div>
            <div className="security-badges">
              <div className="badge">
                <span className="badge-icon">🔒</span>
                <span>Bank-Level Security</span>
              </div>
              <div className="badge">
                <span className="badge-icon">🏆</span>
                <span>Award Winning</span>
              </div>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <div className="footer-bottom-content">
            <div className="legal-links">
              <a href="#privacy">Privacy Policy</a>
              <a href="#terms">Terms of Service</a>
              <a href="#cookies">Cookie Policy</a>
              <a href="#disclosures">Financial Disclosures</a>
            </div>
            <div className="copyright">
              <p>&copy; {currentYear} FinAdvisor AI. All rights reserved.</p>
              <p className="disclaimer">
                Investment advice is provided for educational purposes only. Please consult with a qualified financial advisor.
              </p>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer