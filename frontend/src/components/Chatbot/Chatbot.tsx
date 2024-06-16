'use client';

import MarkdownPreview from '@uiw/react-markdown-preview';
import React, { useEffect, useRef, useState } from 'react';
import UserHeader from '../UserHeader/UserHeader';
import './Chatbot.css';

const Chatbot: React.FC = () => {

    const [ messages, setMessages ] = useState<IMessage[]>([]);
    const [ inputValue, setInputValue ] = useState('');
    const messagesEndRef = useRef<HTMLDivElement | null>(null);
    const [ isLoading, setIsLoading ] = useState(false);
    const [ selectedModel, setSelectedModel ] = useState<'fine-tuned' | 'rag'>('fine-tuned');
    const [ conversationId, setConversationId ] = useState('')

    useEffect(() => {
        setConversationId(Date.now().toString());
    }, [])


    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [ messages ]);

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

        fetch('http://127.0.0.1:5000/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: selectedModel,
                text: inputValue,
                conversation_id: conversationId
            })
        }).then(response => response.json()).then(data => {
            const botMessage: IMessage = {
                text: data.text,
                sender: 'bot',
            };
            setMessages(prevMessages => [ ...prevMessages, botMessage ]);
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
                    setConversationId(Date.now().toString());
                }}
                onLogout={() => {

                }}
                onModelChange={(model) => setSelectedModel(model)}
                selectedModel={selectedModel}
            />
            <div className="main-container">
                <div className="history-container">
                    <h3>History</h3>
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
