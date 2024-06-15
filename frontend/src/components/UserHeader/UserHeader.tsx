'use client';

import React, { useState } from 'react';
import './UserHeader.css';

interface UserHeaderProps {
    onLogout: () => void;
    onClearAll: () => void;
}

const UserHeader: React.FC<UserHeaderProps> = ({ onLogout, onClearAll }) => {
    const [ menuVisible, setMenuVisible ] = useState(false);

    const toggleMenu = () => {
        setMenuVisible(!menuVisible);
    };

    return (
        <div className="user-header">
            <div className="user-info">
                Mental Health Chatbot
            </div>
            <div className="user-menu-container">
                <div className="user-icon" onClick={toggleMenu}>
                    <span>👤</span>
                </div>
                {menuVisible && (
                    <div className="user-menu">
                        <button onClick={onLogout}>Logout</button>
                        <button onClick={onClearAll}>Clear all messages</button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default UserHeader;
