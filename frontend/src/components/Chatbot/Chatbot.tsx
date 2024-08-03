'use client';

import { IConversation } from '@/types/IConversation';
import { IMessage } from '@/types/IMessage';
import { formatDate } from '@/utils/formatDate';
import MarkdownPreview from '@uiw/react-markdown-preview';
import React, { useEffect, useRef, useState } from 'react';
import { Menu, MenuItem, MenuButton } from '@szhsin/react-menu';
import '@szhsin/react-menu/dist/index.css';
import './Chatbot.css';
import { useRouter } from 'next/navigation';
import FeedbackForm from '../FeedbackForm';
import Modal from '../Modal';

const apiUrl = 'http://127.0.0.1:5000'; // Ensure this matches FastAPI URL

const Chatbot: React.FC = () => {
    const [messages, setMessages] = useState<IMessage[]>([]);
    const [inputValue, setInputValue] = useState('');
    const messagesEndRef = useRef<HTMLDivElement | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [selectedModel, setSelectedModel] = useState<'fine-tuned' | 'rag'>('fine-tuned');
    const [conversationId, setConversationId] = useState(0);
    const [history, setHistory] = useState<IConversation[]>([]);
    const [showFeedbackForm, setShowFeedbackForm] = useState(false);
    const [showThankYou, setShowThankYou] = useState(false);
    const router = useRouter(); // For navigation

    // Retrieve the username from localStorage
    const username = typeof window !== 'undefined' ? localStorage.getItem('username') : '';

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    useEffect(() => {
        const loadConversations = async () => {
            try {
                const response = await fetch(`${apiUrl}/api/history`, { headers: { 'Content-Type': 'application/json' } });
                if (!response.ok) {
                    throw new Error(`Error fetching history: ${response.statusText}`);
                }
                const data = await response.json();
                setHistory(data);
            } catch (error) {
                console.error("Error fetching history:", error);
            }
        };
        loadConversations();
    }, []);

    const fetchConversationDetails = async (conversationId: number) => {
        try {
            const response = await fetch(`${apiUrl}/api/conversation/${conversationId}`, { headers: { 'Content-Type': 'application/json' } });
            if (!response.ok) {
                throw new Error(`Error fetching conversation details: ${response.statusText}`);
            }
            const data = await response.json();
            
            const newMessages: IMessage[] = [];
            data.messages.forEach((x: any) => {
                newMessages.push({ text: x.user_message, sender: 'user' });
                newMessages.push({ text: x.bot_response, sender: 'bot' });
            });
            setMessages(newMessages);
            setConversationId(conversationId);
        } catch (error) {
            console.error("Error fetching conversation details:", error);
        }
    };

    const handleSendMessage = () => {
        if (inputValue.trim() === '') return;

        const newMessage: IMessage = {
            text: inputValue,
            sender: 'user',
        };

        setMessages([...messages, newMessage]);
        setInputValue('');
        setIsLoading(true);

        fetch(`${apiUrl}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: selectedModel,
                text: inputValue,
                conversation_id: conversationId,
                user_id: 1 // You might want to replace this with a dynamic user ID
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error sending message: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            const botMessage: IMessage = {
                text: data.text,
                sender: 'bot',
            };
            setMessages(prevMessages => [...prevMessages, botMessage]);
            setConversationId(data.conversation_id);
        })
        .catch(error => {
            console.error("Error sending message:", error);
        })
        .finally(() => {
            setIsLoading(false);
        });
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setInputValue(e.target.value);
    };

    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('username'); // Clear username from local storage on logout
        router.push('/login'); // Navigate to the login page
    };

    const handleNewChat = () => {
        setMessages([]);
        setConversationId(0);
        setShowFeedbackForm(false);
    };

    const handleEndChat = () => {
        setShowFeedbackForm(true);
    };

    const handleFeedbackSubmit = () => {
        setShowFeedbackForm(false);
        setShowThankYou(true);
        setTimeout(() => {
            setShowThankYou(false);
        }, 3000);
    };

    return (
        <div className="chat-wrapper">
            <div className="header">
                <img src="/logo_2.png" alt="Mind2Heart Logo" className="logo" />
                <select
                    value={selectedModel}
                    onChange={(e) => setSelectedModel(e.target.value as 'fine-tuned' | 'rag')}
                    className="model-select"
                >
                    <option value="fine-tuned">Fine-tuned</option>
                    <option value="rag">Rag</option>
                </select>
                <div className="header-right">
                    <span className="username">{username}</span>
                    <Menu menuButton={<MenuButton className="user-button"><img src="/images/user-icon.png" alt="User Icon" className="user-icon" /></MenuButton>}>
                        <MenuItem onClick={handleLogout}>Logout</MenuItem>
                        <MenuItem onClick={handleNewChat}>New chat</MenuItem>
                    </Menu>
                </div>
            </div>
            <div className="main-container">
                <div className="history-container">
                    <h3>History</h3>
                    {history.length === 0 && <p>No history available</p>}
                    {history.map((item, index) => (
                        <div key={index} className='history-item' onClick={() => fetchConversationDetails(item.id)}>
                            <div>
                                <span className='history-item-title'>{item.summary}</span>
                                <small className='history-item-date'>{formatDate(item.timestamp)}</small>
                            </div>
                        </div>
                    ))}
                </div>
                <div className="chat-container">
                    <div className="messages-container">
                        {messages.length === 0 && (
                            <div className="welcome-message">
                                Hello, I am a mental health chatbot. I am here to help you with any questions you may have.
                            </div>
                        )}
                        {messages.map((message, index) => (
                            <div key={index} className={`message-bubble ${message.sender}`}>
                                {message.sender === 'user' && (
                                    <div className="message-sender">{message.text}</div>
                                )}
                                {message.sender === 'bot' && (
                                    <MarkdownPreview
                                        source={message.text || ''}
                                        remarkPlugins={[]}
                                        wrapperElement={{ 'data-color-mode': 'light' }}
                                    />
                                )}
                            </div>
                        ))}
                        {isLoading && <div className="message-bubble bot">Generating response...</div>}
                        <div ref={messagesEndRef}></div>
                    </div>
                    <div className="input-container">
                        <input
                            type="text"
                            value={inputValue}
                            onChange={handleInputChange}
                            onKeyPress={handleKeyPress}
                            placeholder="Type a message..."
                            className="input-message"
                        />
                        <button onClick={handleSendMessage} disabled={isLoading} className="send-button">
                            {isLoading ? 'Sending...' : 'Send'}
                        </button>
                        <button onClick={handleEndChat} className="end-chat-button">
                            End Chat
                        </button>
                    </div>
                    {showFeedbackForm && (
                        <Modal>
                            <FeedbackForm conversationId={conversationId} onSubmit={handleFeedbackSubmit} />
                        </Modal>
                    )}
                    {showThankYou && (
                        <Modal>
                            <h2>Thank you for your feedback!</h2>
                        </Modal>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Chatbot;
