import React from 'react';
import { useHistory } from 'react-router-dom';
import styled from 'styled-components';
import logo from '../../public/logo.png';  // Ensure this path is correct

const Background = styled.div`
  background: url('../../public/background.jpeg') no-repeat center center fixed;  // Ensure this path is correct
  background-size: cover;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  margin-bottom: 2rem;
`;

const StartButton = styled.button`
  padding: 1rem 2rem;
  font-size: 1rem;
  background-color: #007bff;
  border: none;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  &:hover {
    background-color: #0056b3;
  }
`;

const Logo = styled.img`
  width: 200px;
  margin-bottom: 1rem;
`;

const HomePage = () => {
  const history = useHistory();

  const navigateToLogin = () => {
    history.push('/login');
  };

  return (
    <Background>
      <Logo src={logo} alt="Mind2Heart Logo" />
      <Title>Mental Health Advisor</Title>
      <StartButton onClick={navigateToLogin}>Start Chat</StartButton>
    </Background>
  );
};

export default HomePage;
