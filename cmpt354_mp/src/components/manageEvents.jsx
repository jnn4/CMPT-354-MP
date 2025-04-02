import '../App.css';
import React, { useState, useEffect } from 'react';

function ManageEvents() {
    const [events, setEvents] = useState([]);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    // Fetch events when component mounts
    useEffect(() => {
        fetchEvents();
    }, []);

    const fetchEvents = async () => {
        try {
            const response = await fetch('http://localhost:8000/events/');
            if (!response.ok) {
                throw new Error('Failed to fetch events');
            }
            const data = await response.json();
            setEvents(data);
        } catch (error) {
            setError('Error loading events: ' + error.message);
        }
    };

    const handleDelete = async (eventId) => {
        if (!window.confirm('Are you sure you want to delete this event?')) {
            return;
        }

        try {
            const response = await fetch(`http://localhost:8000/events/${eventId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('Failed to delete event');
            }

            setSuccess('Event deleted successfully');
            fetchEvents(); // Refresh the list
        } catch (error) {
            setError('Error deleting event: ' + error.message);
        }
    };

    return (
        <div className="content">
            <h1>Manage Events</h1>
            {error && <p className="error-message">{error}</p>}
            {success && <p className="success-message">{success}</p>}
            
            <div className="events-list">
                {events.map((event) => (
                    <div key={event.event_id} className="event-card">
                        <h3>{event.name}</h3>
                        <p>Type: {event.event_type}</p>
                        <p>Description: {event.description}</p>
                        <p>Date: {event.date}</p>
                        <p>Time: {event.time}</p>
                        <p>Room ID: {event.room_id}</p>
                        <button 
                            className="delete-button"
                            onClick={() => handleDelete(event.event_id)}
                        >
                            Delete
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ManageEvents; 