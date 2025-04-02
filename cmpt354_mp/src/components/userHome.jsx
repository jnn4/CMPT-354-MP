import React, { useEffect, useState } from 'react';
import '../App.css';

function userHome() {
    const user = JSON.parse(localStorage.getItem('loggedInUser'));
    const [volunteerInfo, setVolunteerInfo] = useState(null);
    const [error, setError] = useState('');
    const [borrowedItems, setBorrowedItems] = useState([]);

    useEffect(() => {
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
            const userVolunteer = data.find(v => v.email === user.email);
            if (userVolunteer) {
                setVolunteerInfo(userVolunteer);
            }
        })
        .catch(error => {
            console.error('Error fetching volunteer info:', error);
            setError('Failed to load volunteer information');
        });

        // Fetch user's borrowed items
        fetch(`http://localhost:8000/transactions/`, {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        })
        .then(response => response.json())
        .then(transactions => {
            // Filter transactions for current user and get item details
            const userTransactions = transactions.filter(t => t.user_id === user.user_id);
            const itemPromises = userTransactions.map(transaction => 
                fetch(`http://localhost:8000/items/${transaction.item_id}`)
                    .then(response => response.json())
            );
            return Promise.all(itemPromises);
        })
        .then(items => {
            setBorrowedItems(items);
        })
        .catch(error => {
            console.error('Error fetching borrowed items:', error);
            setError('Failed to load borrowed items');
        });
    }, [user.email, user.user_id]);

    const handleReturnItem = (itemId) => {
        fetch(`http://localhost:8000/items/return/${itemId}`, { 
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                status: 'available'
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Item returned successfully") {
                // Update state to remove returned item
                setBorrowedItems(borrowedItems.filter(item => item.id !== itemId));
            }
        })
        .catch(error => console.error('Error returning item:', error));
    };

    return (
        <div className='content'>
            <h1>Hi {user.name}</h1>
            <p>This is the user dashboard</p>
            
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

            <div className="action-buttons">
                <button className="userHome">View Borrowed Items</button>
                <button className="userHome">Upcoming Events</button>
                <button className="userHome">Volunteering position</button>
            </div>

            <div>
                <h2>Borrowed Items</h2>
                <ul className="items">
                    {borrowedItems.map(item => (
                        <li className="items" key={item.id}>
                            <strong>{item.title}</strong> by {item.author}
                            <button className="items" onClick={() => handleReturnItem(item.id)}>
                                Return
                            </button>
                        </li>
                    ))}
                    {borrowedItems.length === 0 && (
                        <li className="items">You have no borrowed items</li>
                    )}
                </ul>
            </div>
        </div>
    );
}

export default userHome;