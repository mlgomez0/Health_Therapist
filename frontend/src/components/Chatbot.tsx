'use client';

import React, { useState, ChangeEvent, KeyboardEvent } from 'react';

const Chatbot: React.FC = () => {
    const [ messages, setMessages ] = useState<IMessage[]>([]);
    const [ input, setInput ] = useState<string>('');

    const handleSendMessage = () => {
        if (input.trim() === '') return;

        const newMessage: IMessage = {
            text: input,
            sender: 'user',
        };

        setMessages([ ...messages, newMessage ]);
        setInput('');

        fetch('http://127.0.0.1:5000/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: input })
        }).then(response => response.json()).then(data => {
            const botMessage: IMessage = {
                text: data.text,
                sender: 'bot',
            };
            setMessages(prevMessages => [ ...prevMessages, botMessage ]);
        });
    };

    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        setInput(e.target.value);
    };

    const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    };

    return (
        <div className="flex flex-col h-96 w-80 border border-gray-700 rounded-lg overflow-hidden bg-gray-900">
            <div className="flex-1 p-4 overflow-y-auto">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`mb-2 p-2 rounded-lg max-w-xs ${message.sender === 'user' ? 'bg-blue-600 text-white self-end' : 'bg-gray-700 text-gray-300 self-start'}`}
                    >
                        {(message.text || '').split('\n').map((line, index) => <p key={index} style={{ marginBottom: 8 }}>{line}</p>)}
                    </div>
                ))}
            </div>
            <div className="flex border-t border-gray-700">
                <input
                    type="text"
                    value={input}
                    onChange={handleInputChange}
                    onKeyPress={handleKeyPress}
                    placeholder="Type a message..."
                    className="flex-1 p-2 bg-gray-800 text-white border-none outline-none"
                />
                <button
                    onClick={handleSendMessage}
                    className="p-2 bg-blue-600 text-white"
                >
                    Send
                </button>
            </div>
        </div>
    );
};

export default Chatbot;
