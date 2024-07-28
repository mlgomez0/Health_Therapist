'use client';

import React from 'react';
import { Menu, MenuItem, MenuButton } from '@szhsin/react-menu';
import '@szhsin/react-menu/dist/index.css';
import './UserHeader.css';

interface UserHeaderProps {
    username: string;
    onClearAll: () => void;
    onLogout: () => void;
    onModelChange: (model: 'fine-tuned' | 'rag') => void;
    selectedModel: 'fine-tuned' | 'rag';
}

const UserHeader: React.FC<UserHeaderProps> = ({ username, onClearAll, onLogout, onModelChange, selectedModel }) => {
    return (
        <div className="user-header">
            <img src="/logo_2.png" alt="Logo" className="logo" />
            <select value={selectedModel} onChange={(e) => onModelChange(e.target.value as 'fine-tuned' | 'rag')} className="model-select">
                <option value="fine-tuned">Fine-tuned</option>
                <option value="rag">Rag</option>
            </select>
            <div className="user-info">
                <span>{username}</span>
                <Menu menuButton={<MenuButton><img src="/path/to/user-icon.png" alt="User Icon" className="user-icon" /></MenuButton>}>
                    <MenuItem onClick={onLogout}>Logout</MenuItem>
                    <MenuItem onClick={onClearAll}>New Chat</MenuItem>
                </Menu>
            </div>
        </div>
    );
};

export default UserHeader;
