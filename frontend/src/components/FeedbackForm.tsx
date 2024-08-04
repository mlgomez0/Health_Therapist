import React, { useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';

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

const HeartContainer = styled.div`
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;

    .heart {
        cursor: pointer;
        font-size: 2rem;
        color: lightgray;
    }

    .heart.selected {
        color: red;
    }
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

interface FeedbackFormProps {
    conversationId: number;
    onSubmit: () => void;
}

const FeedbackForm: React.FC<FeedbackFormProps> = ({ conversationId, onSubmit }) => {
    const [user_feedback, setFeedback] = useState('');
    const [user_score, setRating] = useState(0);

    const handleFeedbackChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setFeedback(e.target.value);
    };

    const handleRatingChange = (index: number) => {
        setRating(index + 1);
    };

    const handleSubmit = async () => {
        try {
            const username = localStorage.getItem('username');
            await axios.post('http://127.0.0.1:5000/api/feedback', {
                conversation_id: conversationId,
                user_feedback,
                user_score,
            }, {
                headers: { 'x-username': username || '' }
            });
            onSubmit();
        } catch (error) {
            console.error('Error submitting feedback', error);
        }
    };

    return (
        <FeedbackWrapper>
            <FeedbackContainer>
                <h2>Feedback</h2>
                <HeartContainer>
                    {[...Array(5)].map((_, index) => (
                        <span
                            key={index}
                            className={`heart ${index < user_score ? 'selected' : ''}`}
                            onClick={() => handleRatingChange(index)}
                        >
                            ♥
                        </span>
                    ))}
                </HeartContainer>
                <Textarea
                    value={user_feedback}
                    onChange={handleFeedbackChange}
                    placeholder="Please provide your feedback here..."
                />
                <Button onClick={handleSubmit}>Submit</Button>
            </FeedbackContainer>
        </FeedbackWrapper>
    );
};

export default FeedbackForm;
