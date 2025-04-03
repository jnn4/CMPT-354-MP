import React, { useEffect, useState } from 'react';
import './ManageEvents.css';

function ManageEvents() {
    const [events, setEvents] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');
    const [rooms, setRooms] = useState([]);
    const [formData, setFormData] = useState({
        name: '',
        type: '',
        date: '',
        time: '',
        room_id: '',
        audience_type: ''
    });

    useEffect(() => {
        const fetchRooms = async () => {
            try {
                const response = await fetch('http://localhost:8000/events/rooms');
                const data = await response.json();
                setRooms(data);
            } catch (error) {
                console.error('Error fetching rooms:', error);
            }
        };

        fetchRooms();
    }, []);


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

    const handleCreateEvent = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/events/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                alert('Event created successfully!');
                // Refetch events to get full data
                const updatedResponse = await fetch('http://localhost:8000/events');
                const updatedData = await updatedResponse.json();
                setEvents(updatedData);
            } else {
                setErrorMessage(data.message || 'Failed to create event');
            }
        } catch (error) {
            console.error('Error creating event:', error);
            setErrorMessage('Connection error. Please try again.');
        }
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    return (
        <div style={{
            padding: '20px',
            textAlign: 'center',
            maxWidth: '800px',
            margin: '0 auto',
            marginTop: '80px',
        }}>
            <h1 style={{ fontSize: '24px', marginBottom: '20px' }}>Events</h1>
            
            {/* Event Creation Form */}
            <h2 style={{ marginBottom: '20px' }}>Create Event</h2>
            <form onSubmit={handleCreateEvent} style={{ marginBottom: '40px' }}>
                <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Event Name"
                    required
                    style={{ width: '100%', padding: '10px', margin: '10px 0', borderRadius: '5px' }}
                />
                <input
                    type="text"
                    name="type"
                    value={formData.type}
                    onChange={handleChange}
                    placeholder="Event Type"
                    required
                    style={{ width: '100%', padding: '10px', margin: '10px 0', borderRadius: '5px' }}
                />
                <input
                    type="date"
                    name="date"
                    value={formData.date}
                    onChange={handleChange}
                    required
                    style={{ width: '100%', padding: '10px', margin: '10px 0', borderRadius: '5px' }}
                />
                <input
                    type="time"
                    name="time"
                    value={formData.time}
                    onChange={handleChange}
                    required
                    style={{ width: '100%', padding: '10px', margin: '10px 0', borderRadius: '5px' }}
                />
                <input
                    type="number"
                    name="room_id"
                    value={formData.room_id}
                    onChange={handleChange}
                    placeholder="Room ID"
                    required
                    style={{ width: '100%', padding: '10px', margin: '10px 0', borderRadius: '5px' }}
                />
                <input
                    type="text"
                    name="audience_type"
                    value={formData.audience_type}
                    onChange={handleChange}
                    placeholder="Audience Type"
                    required
                    style={{ width: '100%', padding: '10px', margin: '10px 0', borderRadius: '5px' }}
                />
                <button 
                    type="submit"
                    style={{
                        backgroundColor: '#6D6875',
                        color: 'white',
                        padding: '10px 20px',
                        borderRadius: '5px',
                        border: 'none',
                        cursor: 'pointer',
                        width: '50%',
                    }}
                >
                    Create Event
                </button>
            </form>

            <div style={{ padding: '20px', maxWidth: '100%', overflowX: 'auto', whiteSpace: 'nowrap' }}>
                {rooms.map(room => (
                    <div
                        key={room.room_id}
                        style={{
                            display: 'inline-block',
                            marginRight: '20px',
                            padding: '10px',
                            border: '1px solid #ccc',
                            borderRadius: '5px',
                            minWidth: '200px',
                            textAlign: 'center',
                        }}
                    >
                        <h3>{room.name}</h3>
                        <p>Capacity: {room.capacity}</p>
                        <p>Room ID: {room.room_id}</p>
                    </div>
                ))}
            </div>

            {/* Error Message */}
            {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
                        
            {/* Event List */}
            <ul style={{ listStyleType: 'none', padding: '0' }}>
                {events.map(event => (
                    <li
                        key={event.event_id}
                        style={{
                            marginBottom: '10px',
                            padding: '10px',
                            backgroundColor: '#f0f0f0',
                            borderRadius: '5px',
                            display: 'flex',
                            justifyContent: 'space-between',
                        }}
                    >
                        <span>
                            {event.name} ({event.type}) - {event.date}, {event.time}
                            <br />
                            Room: {event.room ? `${event.room.name} (Capacity: ${event.room.capacity})` : 'No room assigned'}
                        </span>
                        <button
                            onClick={() => handleDeleteEvent(event.event_id)}
                            style={{
                                backgroundColor: '#d9534f',
                                color: 'white',
                                border: 'none',
                                borderRadius: '5px',
                            }}
                        >
                            Delete
                        </button>
                    </li>
                ))}
            </ul>   
        </div>
    );
}

export default ManageEvents;
