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
                    <li><a href="/">Home</a></li>
                    <li><a href="/staffHome">Staff Dashboard</a></li>
                    <li><a href="/manage-items">Manage Items</a></li>
                    <li><a href="/manage-events">Manage Events</a></li>
                    <li><a href="/personnel">Personnel</a></li>
                    <li><a href="/volunteer">Volunteer</a></li>
                    <li><a href="/donate">Manage Future Items</a></li>
                    <li><a href="/help-request">Help Requests</a></li>
                </ul>
            </div>
        );
    }

    if (role === 'user') {
        // User-specific navbar
        return (
            <div className="sidebar">
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/userHome">User Dashboard</a></li>
                    <li><a href="/items">Items</a></li>
                    <li><a href="/events">Events</a></li>
                    <li><a href="/personnel">Personnel</a></li>
                    <li><a href="/volunteer">Volunteer</a></li>
                    <li><a href="/donate">Donate Future Items</a></li>
                    <li><a href="/help-request">Help Requests</a></li>
                </ul>
            </div>
        );
    }

    // Default navbar for unauthenticated users or loading state
    return (
        <div className="sidebar">
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/login">Login</a></li>
                <li><a href="/signup">Sign Up</a></li>
            </ul>
        </div>
    );
}

export default Navbar;
