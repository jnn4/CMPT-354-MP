import React, { useEffect, useState } from 'react';
import './navbar.css';

function Navbar() {
    const [role, setRole] = useState('');

    useEffect(() => {
        // Fetch user role from localStorage (or API if required)
        const userRole = localStorage.getItem('userRole'); // 'user' or 'staff'
        setRole(userRole);
    }, []);

    if (role === 'staff') {
        // Staff-specific navbar
        return (
            <div className="sidebar">
                <ul>
                    <a href="/"><li>Home</li></a>
                    <a href="/staffHome"><li>Staff Dashboard</li></a>
                    <a href="/manage-items"><li>Manage Items</li></a>
                    <a href="/manage-events"><li>Manage Events</li></a>
                    <a href="/donate"><li>Manage Future Items</li></a>
                    <a href="/manage-help-requests"><li>Help Requests</li></a>
                </ul>
            </div>
        );
    }

    if (role === 'user') {
        // User-specific navbar
        return (
            <div className="sidebar">
                <ul>
                    <a href="/"><li>Home</li></a>
                    <a href="/userHome"><li>User Dashboard</li></a>
                    <a href="/items"><li>Items</li></a>
                    <a href="/events"><li>Events</li></a>
                    <a href="/donate"><li>Donate Future Items</li></a>
                    <a href="/help-request"><li>Help Requests</li></a>
                </ul>
            </div>
        );
    }

    // Default navbar for unauthenticated users or loading state
    return (
        <div className="sidebar">
            <ul>
                <a href="/"><li>Home</li></a>
                <a href="/login"><li>Login</li></a>
                <a href="/signup"><li>Sign Up</li></a>
            </ul>
        </div>
    );
}

export default Navbar;
