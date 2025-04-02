import React, { useState, useEffect } from 'react';
import '../App.css';

function Events() {
    const [events, setEvents] = useState([]);
    const [searchText, setSearchText] = useState('');
    const [selectedType, setSelectedType] = useState('all');
    const [userEmail, setUserEmail] = useState('');

    // Fetch user email from localStorage on component mount
    useEffect(() => {
        const email = localStorage.getItem('userEmail');
        if (email) setUserEmail(email);
    }, []);

    // Fetch events based on filters
    useEffect(() => {
        let url = `http://localhost:8000/events?search=${searchText}`;
        if (selectedType !== 'all') {
            url += `&type=${selectedType}`;
        }

        fetch(url)
            .then(res => res.json())
            .then(data => setEvents(data))
            .catch(err => console.error("Error fetching events:", err));
    }, [searchText, selectedType]);

    // Handle attending an event
    const handleAttendEvent = async (eventId) => {
        if (!userEmail) {
            alert('Please login to attend events');
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/events/attend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_email: userEmail,
                    event_id: eventId,
                }),
            });

            const data = await response.json();
            if (response.ok) {
                alert(data.message);
            } else {
                alert(data.message || 'Failed to attend the event');
            }
        } catch (err) {
            console.error("Error attending the event:", err);
            alert('An error occurred while attending the event.');
        }
    };

    return (
        <div className="content">
            <h1>Events</h1>

            {/* Search and Filter Controls */}
            <div className="filter-controls">
                <input
                    type="text"
                    placeholder="Search events..."
                    value={searchText}
                    onChange={(e) => setSearchText(e.target.value)}
                />
                <select value={selectedType} onChange={(e) => setSelectedType(e.target.value)}>
                    <option value="all">All Types</option>
                    <option value="workshop">Workshop</option>
                    <option value="seminar">Seminar</option>
                    <option value="meetup">Meetup</option>
                </select>
            </div>

            {/* Events List */}
            <div className="events-list">
                {events.map(event => (
                    <div key={event.event_id} className="event-card">
                        <h3>{event.name}</h3>
                        <p>Type: {event.type}</p>
                        <p>Date: {new Date(event.date).toLocaleDateString()}</p>
                        <p>Time: {event.time}</p>
                        <p>Audience: {event.audience_type}</p>
                        <button onClick={() => handleAttendEvent(event.event_id)}>Attend</button>
                    </div>
                ))}
                {events.length === 0 && (
                    <p>No events found matching your criteria.</p>
                )}
            </div>
        </div>
    );
}

export default Events;