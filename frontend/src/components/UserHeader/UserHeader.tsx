'use client';

import React, { useState } from 'react';
import './UserHeader.css';

interface UserHeaderProps {
    onLogout: () => void;
    onClearAll: () => void;
    selectedModel?: 'fine-tuned' | 'rag';
    onModelChange?: (model: 'fine-tuned' | 'rag') => void;
}

const UserHeader: React.FC<UserHeaderProps> = ({ onLogout, onClearAll, onModelChange, selectedModel }) => {

    const [ menuVisible, setMenuVisible ] = useState(false);

    const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const value = event.target.value as 'fine-tuned' | 'rag';
        onModelChange!(value);
    };

    const toggleMenu = () => {
        setMenuVisible(!menuVisible);
    };

    return (
        <div className="user-header">
            <div className="user-info">
                Mental Health Chatbot
                <select
                    className='model-selector'
                    value={selectedModel}
                    onChange={handleChange}
                >
                    <option value="fine-tuned">Fine-tuned</option>
                    <option value="rag">RAG</option>
                </select>
            </div>
            <div className="user-menu-container">
                <div className="user-icon" onClick={toggleMenu}>
                    <span>👤</span>
                </div>
                {menuVisible && (
                    <div className="user-menu">
                        <button onClick={onLogout}>Logout</button>
                        <button onClick={onClearAll}>New chat</button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UserHeader;
