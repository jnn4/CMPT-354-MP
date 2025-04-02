import React, { useEffect, useState } from 'react';
import '../App.css';

function userHome() {
    const user = JSON.parse(localStorage.getItem('loggedInUser'));
    const [volunteerInfo, setVolunteerInfo] = useState(null);
    const [registeredEvents, setRegisteredEvents] = useState([]);
    const [error, setError] = useState('');

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

        // Fetch user's registered events
        fetch(`http://localhost:8000/events/user/${user.user_id}`)
            .then(response => response.json())
            .then(data => {
                setRegisteredEvents(data);
            })
            .catch(error => {
                console.error('Error fetching registered events:', error);
                setError('Failed to load registered events');
            });
    }, [user.email, user.user_id]);

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

            <div>
                <h2>Borrowed Items</h2>
                <ul className="items">
                    <li className="items">
                        Item Name
                        Author
                        Status
                        <button className="items">Return</button>
                    </li>
                    <li className="items">
                        Item Name
                        Author
                        Status
                        <button className="items">Return</button>
                    </li>
                    <li className="items">
                        Item Name
                        Author
                        Status
                        <button className="items">Return</button>
                    </li>
                </ul>
            </div>
        </div>
    );
}

export default userHome;