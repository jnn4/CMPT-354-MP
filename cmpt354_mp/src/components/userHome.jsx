import React, { useEffect, useState } from 'react';
import '../App.css';

function userHome() {
    const [user, setUser] = useState(null);
    const [volunteerInfo, setVolunteerInfo] = useState(null);
    const [registeredEvents, setRegisteredEvents] = useState([]);
    const [borrowedItems, setBorrowedItems] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        // Get user from localStorage
        const userData = localStorage.getItem('loggedInUser');
        if (!userData) {
            setError('Please log in to view your dashboard');
            return;
        }

        try {
            const parsedUser = JSON.parse(userData);
            setUser(parsedUser);

            // Fetch borrowed items
            fetch(`http://localhost:8000/items/user/${parsedUser.user_id}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch borrowed items');
                    }
                    return response.json();
                })
                .then(data => {
                    setBorrowedItems(data);
                })
                .catch(error => {
                    console.error('Error fetching borrowed items:', error);
                    setError('Failed to load borrowed items');
                });

            // Fetch volunteer information for the current user
            fetch(`http://localhost:8000/volunteer/`, {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Find the volunteer entry for the current user
                const userVolunteer = data.find(v => v.email === parsedUser.email);
                if (userVolunteer) {
                    setVolunteerInfo(userVolunteer);
                }
            })
            .catch(error => {
                console.error('Error fetching volunteer info:', error);
                setError('Failed to load volunteer information');
            });

            // Fetch user's registered events
            fetch(`http://localhost:8000/events/user/${parsedUser.email}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch registered events');
                    }
                    return response.json();
                })
                .then(data => {
                    setRegisteredEvents(data);
                })
                .catch(error => {
                    console.error('Error fetching registered events:', error);
                    setError('Failed to load registered events');
                });
        } catch (error) {
            console.error('Error parsing user data:', error);
            setError('Error loading user data');
        }
    }, []);

    const handleReturnItem = async (itemId) => {
        try {
            const response = await fetch(`http://localhost:8000/items/item/return/${itemId}`, {
                method: 'PATCH'
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.message || 'Failed to return item');
            }

            // Update the borrowed items list by removing the returned item
            setBorrowedItems(borrowedItems.filter(item => item.id !== itemId));
            alert('Item returned successfully!');
        } catch (error) {
            console.error('Error returning item:', error);
            alert(error.message || 'Failed to return item. Please try again.');
        }
    };

    if (!user) {
        return (
            <div className='content'>
                <h1>Error</h1>
                <p>{error}</p>
            </div>
        );
    }

    return (
        <div className='content'>
            <h1>Hi {user.email}</h1>
            <p>This is the user dashboard</p>
            
            {/* Borrowed Items Section */}
            <div className="borrowed-items-section">
                <h2>Your Borrowed Items</h2>
                {borrowedItems.length > 0 ? (
                    <ul className="items">
                        {borrowedItems.map(item => (
                            <li className="items" key={`${item.id}-${item.borrow_date}`}>
                                <strong>{item.title}</strong>
                                <p>Author: {item.author}</p>
                                <p>Borrowed on: {item.borrow_date}</p>
                                <p>Due on: {item.due_date}</p>
                                <button 
                                    className="return-button"
                                    onClick={() => handleReturnItem(item.id)}
                                >
                                    Return Item
                                </button>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>You haven't borrowed any items yet.</p>
                )}
            </div>

            {/* Volunteer Position Section */}
            <div className="volunteer-section">
                <h2>Volunteer Position</h2>
                {volunteerInfo ? (
                    <div className="volunteer-info">
                        <p><strong>Role:</strong> {volunteerInfo.role}</p>
                        <p><strong>Start Date:</strong> {volunteerInfo.start_date}</p>
                        {volunteerInfo.end_date && (
                            <p><strong>End Date:</strong> {volunteerInfo.end_date}</p>
                        )}
                    </div>
                ) : (
                    <p>You are not currently registered as a volunteer.</p>
                )}
                {error && <p className="error-message">{error}</p>}
            </div>

            {/* Registered Events Section */}
            <div>
                <h2>Your Registered Events</h2>
                <ul className="items">
                    {registeredEvents.length > 0 ? (
                        registeredEvents.map(event => (
                            <li className="items" key={event.event_id}>
                                <strong>{event.name}</strong>
                                <p>{event.description}</p>
                                <p>Date: {event.date}</p>
                                <p>Time: {event.time}</p>
                                <p>Room: {event.room_id}</p>
                            </li>
                        ))
                    ) : (
                        <li className="items">You haven't registered for any events yet.</li>
                    )}
                </ul>
            </div>
        </div>
    );
}

export default userHome;