import React, { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import './Navbar.css'

const Navbar = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const location = useLocation()

  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 10
      setScrolled(isScrolled)
    }

    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen)
  }

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false)
  }

  const isActive = (path) => location.pathname === path

  return (
    <>
      <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
        <div className="navbar-container">
          <Link to="/" className="navbar-brand">
            <span className="brand-text">FinAdvisor</span>
            <span className="brand-accent">AI</span>
          </Link>
          
          <div className={`navbar-menu ${isMobileMenuOpen ? 'active' : ''}`}>
            <Link 
              to="/" 
              className={`navbar-link ${isActive('/') ? 'active' : ''}`}
              onClick={closeMobileMenu}
            >
              Home
            </Link>
            <Link 
              to="/profile" 
              className={`navbar-link ${isActive('/profile') ? 'active' : ''}`}
              onClick={closeMobileMenu}
            >
              Profile
            </Link>
            <Link 
              to="/recommendations" 
              className={`navbar-link ${isActive('/recommendations') ? 'active' : ''}`}
              onClick={closeMobileMenu}
            >
              Recommendations
            </Link>
            <Link 
              to="/dashboard" 
              className={`navbar-link ${isActive('/dashboard') ? 'active' : ''}`}
              onClick={closeMobileMenu}
            >
              Dashboard
            </Link>
          </div>

          <button 
            className={`mobile-menu-toggle ${isMobileMenuOpen ? 'active' : ''}`}
            onClick={toggleMobileMenu}
            aria-label="Toggle menu"
            aria-expanded={isMobileMenuOpen}
          >
            <span className="hamburger-line"></span>
            <span className="hamburger-line"></span>
            <span className="hamburger-line"></span>
          </button>
        </div>

        {/* Mobile menu backdrop */}
        {isMobileMenuOpen && (
          <div 
            className="mobile-backdrop"
            onClick={closeMobileMenu}
          />
        )}
      </nav>

      <style jsx>{`
        .navbar {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          z-index: 1000;
          background: rgba(0, 0, 0, 0.95);
          backdrop-filter: blur(20px);
          border-bottom: 1px solid rgba(75, 85, 99, 0.3);
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .navbar.scrolled {
          background: rgba(0, 0, 0, 0.98);
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
          border-bottom: 1px solid rgba(75, 85, 99, 0.5);
        }

        .navbar-container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 24px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          height: 70px;
        }

        .navbar-brand {
          display: flex;
          align-items: center;
          gap: 2px;
          font-size: 24px;
          font-weight: 700;
          text-decoration: none;
          padding: 8px 12px;
          border-radius: 12px;
          transition: all 0.2s ease;
        }

        .navbar-brand:hover {
          background: rgba(16, 185, 129, 0.1);
          transform: translateY(-1px);
        }

        .brand-text {
          color: #f9fafb;
          letter-spacing: -0.5px;
        }

        .brand-accent {
          color: #10b981;
          font-weight: 800;
        }

        .navbar-menu {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .navbar-link {
          position: relative;
          padding: 10px 20px;
          font-size: 15px;
          font-weight: 500;
          color: #d1d5db;
          text-decoration: none;
          border-radius: 12px;
          transition: all 0.2s ease;
          letter-spacing: -0.2px;
        }

        .navbar-link:hover {
          color: #10b981;
          background: rgba(16, 185, 129, 0.1);
          transform: translateY(-1px);
        }

        .navbar-link.active {
          color: #10b981;
          background: rgba(16, 185, 129, 0.15);
          font-weight: 600;
        }

        .navbar-link.active::after {
          content: '';
          position: absolute;
          bottom: 6px;
          left: 50%;
          transform: translateX(-50%);
          width: 20px;
          height: 2px;
          background: #10b981;
          border-radius: 1px;
        }

        .mobile-menu-toggle {
          display: none;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          width: 44px;
          height: 44px;
          background: none;
          border: none;
          cursor: pointer;
          border-radius: 12px;
          transition: all 0.2s ease;
          gap: 4px;
        }

        .mobile-menu-toggle:hover {
          background: rgba(16, 185, 129, 0.1);
        }

        .hamburger-line {
          width: 20px;
          height: 2px;
          background: #d1d5db;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          border-radius: 1px;
        }

        .mobile-menu-toggle.active .hamburger-line:nth-child(1) {
          transform: rotate(45deg) translate(5px, 5px);
        }

        .mobile-menu-toggle.active .hamburger-line:nth-child(2) {
          opacity: 0;
        }

        .mobile-menu-toggle.active .hamburger-line:nth-child(3) {
          transform: rotate(-45deg) translate(7px, -6px);
        }

        .mobile-backdrop {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.5);
          z-index: 998;
          backdrop-filter: blur(4px);
        }

        @media (max-width: 768px) {
          .navbar-container {
            padding: 0 16px;
            height: 60px;
          }

          .navbar-brand {
            font-size: 20px;
          }

          .mobile-menu-toggle {
            display: flex;
          }

          .navbar-menu {
            position: fixed;
            top: 60px;
            right: 0;
            width: 280px;
            max-width: 100vw;
            height: calc(100vh - 60px);
            background: #000000;
            flex-direction: column;
            align-items: stretch;
            padding: 24px;
            gap: 8px;
            transform: translateX(100%);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: -4px 0 20px rgba(0, 0, 0, 0.3);
            z-index: 999;
          }

          .navbar-menu.active {
            transform: translateX(0);
          }

          .navbar-link {
            padding: 16px 20px;
            font-size: 16px;
            text-align: left;
            border-radius: 16px;
            width: 100%;
          }

          .navbar-link.active::after {
            display: none;
          }

          .navbar-link.active {
            background: rgba(16, 185, 129, 0.1);
            border-left: 3px solid #10b981;
            border-radius: 0 16px 16px 0;
          }
        }

        @media (max-width: 480px) {
          .navbar-container {
            padding: 0 12px;
          }

          .navbar-menu {
            width: 100vw;
            right: 0;
            padding: 20px;
          }
        }
      `}</style>
    </>
  )
}

export default Navbar