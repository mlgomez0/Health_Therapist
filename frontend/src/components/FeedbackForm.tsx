import React, { useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import Modal from './Modal';

const FeedbackWrapper = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: #f9f9f9;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    max-width: 600px;
    margin: 2rem auto;
`;

const FeedbackContainer = styled.div`
    width: 100%;
`;

const Textarea = styled.textarea`
    width: 100%;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 5px;
    border: 1px solid #ccc;
`;

const Button = styled.button`
    padding: 0.5rem 2rem;
    background-color: #007bff;
    border: none;
    color: white;
    border-radius: 5px;
    cursor: pointer;
    &:hover {
        background-color: #0056b3;
    }
`;

const HeartsContainer = styled.div`
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;
`;

const Heart = styled.span<{ selected: boolean }>`
    font-size: 2rem;
    cursor: pointer;
    color: ${props => (props.selected ? 'red' : 'lightgray')};
    transition: color 0.3s;

    &:hover {
        color: red;
    }
`;

interface FeedbackFormProps {
    conversationId: number;
    onSubmit: () => void;
}

const FeedbackForm: React.FC<FeedbackFormProps> = ({ conversationId, onSubmit }) => {
    const [feedback, setFeedback] = useState('');
    const [rating, setRating] = useState(0);
    const [showThankYou, setShowThankYou] = useState(false);

    const handleFeedbackChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setFeedback(e.target.value);
    };

    const handleRatingChange = (index: number) => {
        setRating(index + 1);
    };

    const handleSubmit = async () => {
        try {
            const username = localStorage.getItem('username');
            await axios.post('http://localhost:5000/api/feedback', {
                conversation_id: conversationId,
                feedback,
                rating,
            }, {
                headers: { 'x-username': username || '' }
            });
            setShowThankYou(true);
            setTimeout(() => {
                setShowThankYou(false);
                onSubmit();
            }, 3000);
        } catch (error) {
            console.error('Error submitting feedback', error);
        }
    };

    return (
        <FeedbackWrapper>
            <FeedbackContainer>
                <h2>Feedback</h2>
                <HeartsContainer>
                    {[...Array(5)].map((_, index) => (
                        <Heart
                            key={index}
                            selected={index < rating}
                            onClick={() => handleRatingChange(index)}
                        >
                            ♥
                        </Heart>
                    ))}
                </HeartsContainer>
                <Textarea
                    value={feedback}
                    onChange={handleFeedbackChange}
                    placeholder="Please provide your feedback here..."
                />
                <Button onClick={handleSubmit}>Submit</Button>
            </FeedbackContainer>
            {showThankYou && (
                <Modal>
                    <h2>Thank you for your feedback!</h2>
                </Modal>
            )}
        </FeedbackWrapper>
    );
};

export default FeedbackForm;
