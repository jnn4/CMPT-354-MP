import React, { useEffect, useState } from 'react';

function ManageEvents() {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        const fetchEvents = async () => {
            const response = await fetch('http://localhost:8000/events');
            const data = await response.json();
            setEvents(data);
        };

        fetchEvents();
    }, []);

    const handleDeleteEvent = async (eventId) => {
        try {
            const response = await fetch(`http://localhost:8000/events/delete/${eventId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                alert('Event deleted successfully!');
                setEvents(events.filter(event => event.event_id !== eventId));
            } else {
                alert('Failed to delete event.');
            }
        } catch (error) {
            console.error('Error deleting event:', error);
            alert('An error occurred while deleting the event.');
        }
    };

    return (
        <div>
            <h1>Events</h1>
            <ul>
                {events.map(event => (
                    <li key={event.event_id}>
                        {event.name} ({event.type}) in Room: {event.room?.room_ || 'No room'}
                        <button onClick={() => handleDeleteEvent(event.event_id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ManageEvents;
