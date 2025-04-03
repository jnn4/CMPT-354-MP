import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './navbar.css';

function Navbar() {
    const [current, setCurrent] = useState('home');
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        // Check if user is logged in
        const loggedInUser = localStorage.getItem('loggedInUser');
        if (loggedInUser) {
            setUser(JSON.parse(loggedInUser));
        }
    }, []);

    const handleLogout = async () => {
        try {
            // Call logout endpoint
            const response = await fetch('http://localhost:8000/users/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            // Even if the backend request fails, we'll still log out the user locally
            // Clear user data from localStorage
            localStorage.removeItem('loggedInUser');
            setUser(null);
            
            // Navigate to login page
            navigate('/login');
        } catch (error) {
            console.error('Error during logout:', error);
            // Still log out the user locally even if the backend request fails
            localStorage.removeItem('loggedInUser');
            setUser(null);
            navigate('/login');
        }
    };

    return (
        <div className="sidebar">
            {user ? (
                // Logged in user view
                <>
                    <div className="user-info">
                        <p>Welcome, {user.name}</p>
                        <p className="role">{user.role === 'staff' ? 'Staff Member' : 'User'}</p>
                    </div>
                    <ul>
                        {/* <li><a href="/">Home</a></li> */}
                        {user.role !== 'staff' && <li><a href="/userHome">User Home</a></li>}
                        {user.role !== 'staff' && (
                            <>
                                <li><a href="/items">Items</a></li>
                                <li><a href="/events">Events</a></li>
                                <li><a href="/volunteer">Volunteer</a></li>
                                <li><a href="/donate">Donate</a></li>
                                <li><a href="/contact">Contact</a></li>
                            </>
                        )}
                        {user.role === 'staff' && (
                            <>
                                <li><a href="/manage-items">Manage Items</a></li>
                                <li><a href="/manage-events">Manage Events</a></li>
                                <li><a href="/manage-fines">Manage Fines</a></li>
                                <li><a href="/manage-staff">Manage Staff</a></li>
                                <li><a href="/manage-volunteers">Manage Volunteers</a></li>
                            </>
                        )}
                        <li className="logout-button" onClick={handleLogout}>Log out</li>
                    </ul>
                </>
            ) : (
                // Not logged in view
                <>
                    <div className="user-info">
                        <p>Welcome to Library</p>
                        <p className="role">Please log in to continue</p>
                    </div>
                    <ul>
                        {/* <li><a href="/">Home</a></li> */}
                        {user ? (
                            <>
                                {user.role !== 'staff' && (
                                    <>
                                        <li><a href="/userHome">User Home</a></li>
                                        <li><a href="/items">Items</a></li>
                                        <li><a href="/events">Events</a></li>
                                        <li><a href="/volunteer">Volunteer</a></li>
                                        <li><a href="/donate">Donate</a></li>
                                        <li><a href="/contact">Contact</a></li>
                                    </>
                                )}
                                {user.role === 'staff' && (
                                    <>
                                        <li><a href="/manage-items">Manage Items</a></li>
                                        <li><a href="/manage-events">Manage Events</a></li>
                                        <li><a href="/manage-fines">Manage Fines</a></li>
                                        <li><a href="/manage-staff">Manage Staff</a></li>
                                        <li><a href="/manage-volunteers">Manage Volunteers</a></li>
                                    </>
                                )}
                                <li className="logout-button" onClick={handleLogout}>Log out</li>
                            </>
                        ) : (
                            <>
                                <li><a href="/">Home</a></li>
                                <li><a href="/items">Items</a></li>
                                <li><a href="/events">Events</a></li>
                                <li><a href="/login">Login</a></li>
                                <li><a href="/signup">Sign Up</a></li>
                            </>
                        )}
                    </ul>
                </>
            )}
        </div>
    );
}

export default Navbar;