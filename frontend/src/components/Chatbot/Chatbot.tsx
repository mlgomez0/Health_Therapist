'use client';

import { IConversation } from '@/types/IConversation';
import { formatDate } from '@/utils/formatDate';
import MarkdownPreview from '@uiw/react-markdown-preview';
import React, { useEffect, useRef, useState } from 'react';
import UserHeader from '../UserHeader/UserHeader';
import './Chatbot.css';

const apiUrl = 'http://127.0.0.1:5000'

const Chatbot: React.FC = () => {

    const [ messages, setMessages ] = useState<IMessage[]>([]);
    const [ inputValue, setInputValue ] = useState('');
    const messagesEndRef = useRef<HTMLDivElement | null>(null);
    const [ isLoading, setIsLoading ] = useState(false);
    const [ selectedModel, setSelectedModel ] = useState<'fine-tuned' | 'rag'>('fine-tuned');
    const [ conversationId, setConversationId ] = useState(0);
    const [ history, setHistory ] = useState<IConversation[]>([]);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [ messages ]);

    useEffect(() => {
        const loadConverstations = async () => {
            const response = await fetch(`${apiUrl}/api/history`, { headers: { 'Content-Type': 'application/json' } });
            const data = await response.json();
            setHistory(data);
        }
        loadConverstations();
    }, []);

    const handleSendMessage = () => {

        if (inputValue.trim() === '')
            return;

        const newMessage: IMessage = {
            text: inputValue,
            sender: 'user',
        };

        setMessages([ ...messages, newMessage ]);
        setInputValue('');
        setIsLoading(true);

        fetch(`${apiUrl}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: selectedModel,
                text: inputValue,
                conversation_id: conversationId,
                user_id: 1
            })
        }).then(response => response.json()).then(data => {
            const botMessage: IMessage = {
                text: data.text,
                sender: 'bot',
            };
            setMessages(prevMessages => [ ...prevMessages, botMessage ]);
            setConversationId(data.conversation_id);
        }).finally(() => {
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

    return (
        <div className="chat-wrapper">
            <UserHeader
                onClearAll={() => {
                    setMessages([]);
                    setConversationId(0);
                }}
                onLogout={() => {

                }}
                onModelChange={(model) => setSelectedModel(model)}
                selectedModel={selectedModel}
            />
            <div className="main-container">
                <div className="history-container">
                    <h3>History</h3>
                    {history.map((item, index) => <div key={index} className='history-item'>
                        <div>
                            <span className='history-item-title'>
                                {item.model_name}
                            </span>
                            <br />
                            <small className='history-item-date'>
                                {formatDate(item.timestamp)}
                            </small>
                        </div>
                    </div>)}
                </div>
                <div className="chat-container">
                    <div className="messages-container">
                        {messages.length === 0 && <>
                            <div className="welcome-message">
                                Hello, I am a mental health chatbot. I am here to help you with any questions you may have.
                            </div>
                        </>}
                        {messages.map((message, index) => (
                            <div key={index} className={`message-bubble ${message.sender}`}>
                                {message.sender === 'user' && <div className="message-sender">
                                    {message.text}
                                </div>}
                                {message.sender === 'bot' && <MarkdownPreview
                                    source={message.text || ''} remarkPlugins={[]}
                                    wrapperElement={{
                                        'data-color-mode': 'light'
                                    }}
                                />}
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
                        />
                        <button
                            onClick={handleSendMessage}
                            disabled={isLoading}
                        >
                            {isLoading ? 'Sending...' : 'Send'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Chatbot;
