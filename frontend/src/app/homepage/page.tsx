"use client";
import React from 'react';
import { useRouter } from 'next/navigation';
import styled from 'styled-components';

const PageWrapper = styled.div`
  width: 100%;
  height: 100%;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const Background = styled.div`
  background: url('/backgound.jpg') no-repeat center center;
  background-size: cover;
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
  position: relative;
`;

const Logo = styled.img`
  position: absolute;
  top: 1px;
  left: 5px;
  width: 250px; /* Adjust size as needed */
  height: auto; /* Maintain aspect ratio */
`;

const Spacer = styled.div`
  height: 50vh; /* Add extra space to ensure scrolling */
`;

const ContentWrapper = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  background-color: #f4f4f9;
`;

const Content = styled.div`
  padding: 2rem;
  background-color: white;
  color: #333;
  text-align: left;
  width: 100%;
  max-width: 800px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  margin-bottom: 2rem;
`;

const StartButton = styled.button`
  padding: 1rem 2rem;
  font-size: 1rem;
  font-weight: bold;
  background-color: #4DA9DF;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  &:hover {
    background-color: #0056b3;
  }
`;

const Phrase = styled.h2`
  font-family: 'Public Sans', sans-serif;
  font-size: 70px;
  color: #3795CB;
  margin-bottom: 1rem;
  text-align: center;
`;

const SubTitle = styled.h3`
  font-family: 'Public Sans', sans-serif;
  font-size: 24px;
  color: #3795CB;
  margin-bottom: 1rem;
  text-align: center;
`;

const Paragraph = styled.p`
  font-family: 'Public Sans', sans-serif;
  font-size: 18px;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  text-align: justify;
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

const SocialIcon = styled.img`
  margin: 0 0.5rem;
  width: auto; /* Adjust size as needed */
  height: 50px;
`;

const ButtonWrapper = styled.div`
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 1rem;
`;

const NavButton = styled.button`
  padding: 0.5rem 1rem;
  font-size: 1rem;
  background-color: #4DA9DF;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  &:hover {
    background-color: #0056b3;
  }
`;

const HomePage = () => {
  const router = useRouter();

  const navigateToLogin = () => {
    router.push('/login');
  };

  const navigateToRegister = () => {
    router.push('/register');
  };

  return (
    <PageWrapper>
      <Background>
        <Logo src="/logo.png" alt="Mind2Heart Logo" />
        <ButtonWrapper>
          <NavButton onClick={navigateToLogin}>Login</NavButton>
          <NavButton onClick={navigateToRegister}>Signup</NavButton>
        </ButtonWrapper>
        <div style={{ position: "absolute", bottom: "2rem", left: "50%", transform: "translateX(-50%)" }}>
          <StartButton onClick={navigateToLogin}>Start Chat</StartButton>
        </div>
      </Background>
      <Spacer /> {/* Adds extra space to ensure scrolling */}
      <ContentWrapper>
        <Phrase>BRIDGING MINDS HEALING HEARTS</Phrase>
        <Content>
          <SubTitle>About Us</SubTitle>
          <Paragraph>
            Welcome to Mind2Heart, where we prioritize mental health and wellbeing. Our mission is to provide accessible and effective mental health support through innovative technology and compassionate care. Whether you're looking for professional advice, self-help resources, or a supportive community, Mind2Heart is here to help you on your journey to better mental health.
          </Paragraph>
          <Paragraph>
            At Mind2Heart, we believe that mental health is just as important as physical health. Our team of experts is dedicated to offering a wide range of services designed to meet the diverse needs of our users. From therapy sessions to mindfulness exercises, we are committed to providing the tools and support you need to thrive.
          </Paragraph>
        </Content>
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
          <SocialIcon src="/images/appstore.png" alt="App Store" />
          <SocialIcon src="/images/googleplay.png" alt="Google Play" />
          <SocialIcon src="/images/facebook.png" alt="Facebook" />
          <SocialIcon src="/images/twitter.png" alt="Twitter" />
          <SocialIcon src="/images/youtube.png" alt="YouTube" />
          <SocialIcon src="/images/linkedin.png" alt="LinkedIn" />
          <SocialIcon src="/images/pinterest.png" alt="Pinterest" />
        </SocialIcons>
        <div>© 2024 Mind2Heart Inc. All Rights Reserved.</div>
      </Footer>
    </PageWrapper>
  );
};

export default HomePage;
