"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import styled from 'styled-components';
import axios from 'axios';

// Styled components
const PageWrapper = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
`;

const ContentWrapper = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #0E6DA6;
  padding: 2rem 0;
`;

const SplitContainer = styled.div`
  display: flex;
  width: 800px;
  background-color: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
`;

const LogoSide = styled.div`
  background-color: #e6f7ff;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
`;

const LogoImage = styled.img`
  width: 300px;
  height: auto;
  margin-bottom: 1rem;
`;

const FormSide = styled.div`
  flex: 1.5;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.8);
`;

const Form = styled.form`
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
`;

const InputWrapper = styled.div`
  position: relative;
  width: 80%;
  margin: 0.5rem 0;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 5px;
`;

const Button = styled.button`
  padding: 0.5rem 2rem;
  font-size: 1rem;
  background-color: #007bff;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  margin: 0.5rem 0;
  &:hover {
    background-color: #0056b3;
  }
`;

const RegisterContainer = styled.div`
  display: flex;
  align-items: center;
  margin-top: 1rem;
  justify-content: center;
`;

const RegisterText = styled.p`
  margin: 0;
  color: #000;
`;

const RegisterLink = styled.a`
  margin-left: 0.5rem;
  color: #007bff;
  text-decoration: none;
  &:hover {
    text-decoration: underline;
  }
`;

const ForgotPasswordLink = styled.a`
  display: block;
  margin-top: 0.5rem;
  color: #007bff;
  text-decoration: none;
  &:hover {
    text-decoration: underline;
  }
`;

const SocialButton = styled.a`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  margin: 0.5rem;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 20px;
  color: #fff;
  border-radius: 50%;
  text-decoration: none;

  &:hover {
    opacity: 0.8;
  }
`;

const FacebookButton = styled(SocialButton)`
  background-color: #3b5998;
`;

const GoogleButton = styled(SocialButton)`
  background-color: #db4437;
`;

const LinkedInButton = styled(SocialButton)`
  background-color: #0077b5;
`;

const SocialContainer = styled.div`
  display: flex;
  justify-content: center;
  margin: 1rem 0;
`;

const MaskIcon = styled.img`
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  cursor: pointer;
  width: 20px;
  height: 20px;
`;

const Footer = styled.footer`
  width: 100%;
  background-color: #fff;
  padding: 1rem 2rem;
  text-align: center;
  box-shadow: 0 -1px 4px rgba(0, 0, 0, 0.1);
`;

const FooterLinks = styled.div`
  margin: 1rem 0;
`;

const FooterLink = styled.a`
  margin: 0 0.5rem;
  color: #0073e6;
  text-decoration: none;
  &:hover {
    text-decoration: underline;
  }
`;

const SocialIcons = styled.div`
  margin: 1rem 0;
`;

const FooterSocialIcon = styled.img`
  margin: 0 0.5rem;
  width: auto;
  height: 50px;
`;

const LoginPage = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const router = useRouter();

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:5000/api/login', {
        username,
        password
      });

      if (response.status === 200) {
        setMessage('Login successful');
        const { user_id } = response.data;
        localStorage.setItem('username', username); // Save username to localStorage
        localStorage.setItem('user_id', user_id); // Save user_id to localStorage
        router.push('/chat'); // Navigate to the home page on successful login
      } else {
        setMessage(response.data.detail || 'Invalid username or password');
      }
    } catch (error) {
      if (axios.isAxiosError(error) && error.response && error.response.data && error.response.data.detail) {
        setMessage(error.response.data.detail);
      } else {
        setMessage('Login failed. Please try again.');
      }
    }
  };

  return (
    <PageWrapper>
      <ContentWrapper>
        <SplitContainer>
          <LogoSide>
            <LogoImage src="/logo_2.png" alt="Mind2Heart Logo" />
          </LogoSide>
          <FormSide>
            <Form onSubmit={handleLogin}>
              <h2>Login</h2>
              {/* <SocialContainer>
                <FacebookButton href="https://www.facebook.com/login" target="_blank" rel="noopener noreferrer">f</FacebookButton>
                <GoogleButton href="https://accounts.google.com/signin" target="_blank" rel="noopener noreferrer">G+</GoogleButton>
                <LinkedInButton href="https://www.linkedin.com/login" target="_blank" rel="noopener noreferrer">in</LinkedInButton>
              </SocialContainer> */}
              <p>or use your username to login:</p>
              <InputWrapper>
                <Input
                  type="text"
                  placeholder="Username"
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </InputWrapper>

              <InputWrapper>
                <Input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </InputWrapper>
              {/*<ForgotPasswordLink href="/forgot-password">Forgot password?</ForgotPasswordLink>*/}
              <Button type="submit">Login</Button>
              {message && <p>{message}</p>}
              <RegisterContainer>
                <RegisterText>Not on Mind2Heart yet?</RegisterText>
                <RegisterLink href="/register">Create new account</RegisterLink>
              </RegisterContainer>
            </Form>
          </FormSide>
        </SplitContainer>
      </ContentWrapper>
      <Footer>
        <FooterLinks>
          <FooterLink href="#">Legal Center</FooterLink>
          <FooterLink href="#">Trust Center</FooterLink>
          <FooterLink href="#">Privacy</FooterLink>
          <FooterLink href="#">Cookie Preferences</FooterLink>
          <FooterLink href="#">Accessibility</FooterLink>
        </FooterLinks>
        <SocialIcons>
          <FooterSocialIcon src="/images/appstore.png" alt="App Store" />
          <FooterSocialIcon src="/images/googleplay.png" alt="Google Play" />
          <FooterSocialIcon src="/images/facebook.png" alt="Facebook" />
          <FooterSocialIcon src="/images/twitter.png" alt="Twitter" />
          <FooterSocialIcon src="/images/youtube.png" alt="YouTube" />
          <FooterSocialIcon src="/images/linkedin.png" alt="LinkedIn" />
          <FooterSocialIcon src="/images/pinterest.png" alt="Pinterest" />
        </SocialIcons>
        <p>&copy; 2024 Mind2Heart Inc. All Rights Reserved.</p>
      </Footer>
    </PageWrapper>
  );
};

export default LoginPage;
