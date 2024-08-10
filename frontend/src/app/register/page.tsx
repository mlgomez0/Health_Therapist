"use client";

import React, { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import './Register.css';

const Register: React.FC = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const router = useRouter();

  const handleRegister = async (event: React.FormEvent) => {
    event.preventDefault();
    if (password !== confirmPassword) {
      setMessage("Passwords do not match");
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/api/register', { username, email, password });
      setMessage(response.data.message);
      if (response.data.message === "Registration successful") {
        window.location.href = '/login'; // Navigate to login page on successful registration
      }
    } catch (error: any) {
      if (axios.isAxiosError(error) && error.response && error.response.data && error.response.data.detail) {
        setMessage(error.response.data.detail);
      } else {
        setMessage('Registration failed. Please try again.');
      }
    }
  };

  const handleSignInClick = () => {
    // Navigate to the login page
    router.push('/login');
  };

  return (
    <div id="root">
      <div className="register-container">
        <div className="welcome-section">
          <img src="/logo.png" alt="Mind2Heart Logo" className="logo" />
          <p>To keep connected with us please login with your personal info</p>
        </div>
        <div className="register-section">
          <h2>Create Account</h2>
          {/* <div className="social-buttons">
            <a href="https://www.facebook.com/login" className="social-btn facebook" target="_blank" rel="noopener noreferrer">f</a>
            <a href="https://accounts.google.com/signin" className="social-btn google" target="_blank" rel="noopener noreferrer">G+</a>
            <a href="https://www.linkedin.com/login" className="social-btn linkedin" target="_blank" rel="noopener noreferrer">in</a>
          </div> */}
          <p>or use your email for registration:</p>
          <form className="register-form" onSubmit={handleRegister}>
            <div className="form-group">
              <input
                type="text"
                placeholder="Username"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <input
                type="email"
                placeholder="Email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <input
                type="password"
                placeholder="Password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <input
                type="password"
                placeholder="Confirm Password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
            <div className="checkbox-group">
              <input type="checkbox" id="terms" required />
              <label htmlFor="terms">I agree to all statements in <a href="#">Terms of service</a></label>
            </div>
            <div className="sign-up-btn">
              <button type="submit">Sign Up</button>
            </div>
          </form>
          {message && <p>{message}</p>}
          <p>Have already an account? <a href="/login">Login here</a></p>
        </div>
      </div>
      <footer className="footer">
        <div className="footer-links">
          <a href="#">Legal Center</a>
          <a href="#">Trust Center</a>
          <a href="#">Privacy</a>
          <a href="#">Cookie Preferences</a>
          <a href="#">Accessibility</a>
        </div>
        <div className="footer-icons">
          <a href="#"><img src="/images/appstore.png" alt="App Store" /></a>
          <a href="#"><img src="/images/googleplay.png" alt="Google Play" /></a>
          <a href="#"><img src="/images/facebook.png" alt="Facebook" /></a>
          <a href="#"><img src="/images/twitter.png" alt="Twitter" /></a>
          <a href="#"><img src="/images/youtube.png" alt="YouTube" /></a>
          <a href="#"><img src="/images/linkedin.png" alt="LinkedIn" /></a>
          <a href="#"><img src="/images/pinterest.png" alt="Pinterest" /></a>
        </div>
        <p>&copy; 2024 Mind2Heart Inc. All Rights Reserved.</p>
      </footer>
    </div>
  );
};

export default Register;
