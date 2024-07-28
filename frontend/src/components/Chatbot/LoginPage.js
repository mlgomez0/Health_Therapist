import React from 'react';
import styled from 'styled-components';

const LoginPageWrapper = styled.div`
  background: url('../../public/background.jpeg') no-repeat center center fixed;  // Ensure this path is correct
  background-size: cover;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

const Form = styled.form`
  background: rgba(255, 255, 255, 0.8);
  padding: 2rem;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 300px;
  text-align: center;
`;

const Input = styled.input`
  width: 100%;
  padding: 0.5rem;
  margin: 0.5rem 0;
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
  &:hover {
    background-color: #0056b3;
  }
`;

const LoginPage = () => {
  return (
    <LoginPageWrapper>
      <Form>
        <h2>Login</h2>
        <Input type="text" placeholder="Username" />
        <Input type="password" placeholder="Password" />
        <Button type="submit">Login</Button>
      </Form>
    </LoginPageWrapper>
  );
};

export default LoginPage;
