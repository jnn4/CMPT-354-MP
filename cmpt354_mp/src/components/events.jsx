import React, { useState, useEffect } from 'react';
import '../App.css';

function Events() {
    const [events, setEvents] = useState([]);
    const [searchText, setSearchText] = useState('');
    const [selectedType, setSelectedType] = useState('all');
    const [userEmail, setUserEmail] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    // Debounce search input
    const debounce = (func, delay) => {
        let timer;
        return (...args) => {
            clearTimeout(timer);
            timer = setTimeout(() => func(...args), delay);
        };
    };

    // Fetch user email on mount
    useEffect(() => {
        const email = localStorage.getItem('userEmail');
        if (email) setUserEmail(email);
    }, []);

    // Fetch events with error handling and cleanup
    useEffect(() => {
        const controller = new AbortController();
        const { signal } = controller;
        
        const fetchEvents = async () => {
            setLoading(true);
            try {
                let url = `http://localhost:8000/events?search=${encodeURIComponent(searchText)}`;
                if (selectedType !== 'all') {
                    url += `&type=${encodeURIComponent(selectedType)}`;
                }

                const response = await fetch(url, { signal });
                if (!response.ok) throw new Error('Failed to fetch events');
                
                const data = await response.json();
                setEvents(data);
                setError('');
            } catch (err) {
                if (err.name !== 'AbortError') {
                    setError('Failed to load events. Please try again later.');
                    console.error("Error fetching events:", err);
                }
            } finally {
                setLoading(false);
            }
        };

        const debouncedFetch = debounce(fetchEvents, 300);
        debouncedFetch();

        return () => controller.abort();
    }, [searchText, selectedType]);

    // Handle event attendance
    const handleAttendEvent = async (eventId) => {
        if (!userEmail) {
            alert('Please login to attend events');
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/events/attend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_email: userEmail, event_id: eventId }),
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.message || 'Failed to attend event');
            
            alert(data.message);
            // Refresh events after successful attendance
            setEvents(prev => prev.map(event => 
                event.event_id === eventId ? { ...event, attended: true } : event
            ));
        } catch (err) {
            console.error("Error attending event:", err);
            alert(err.message || 'An error occurred');
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
                    aria-label="Search events"
                />
                <select 
                    value={selectedType} 
                    onChange={(e) => setSelectedType(e.target.value)}
                    aria-label="Filter events by type"
                >
                    <option value="all">All Types</option>
                    <option value="workshop">Workshop</option>
                    <option value="seminar">Seminar</option>
                    <option value="meetup">Meetup</option>
                </select>
            </div>

            {/* Loading and Error States */}
            {loading && <p className="status-message">Loading events...</p>}
            {error && <p className="error-message">{error}</p>}

            {/* Events List */}
            <div className="events-list">
                {events.map(event => (
                    <div key={event.event_id} className="event-card">
                        <h3>{event.name}</h3>
                        <div className="event-details">
                            <p>Type: {event.type}</p>
                            <p>Date: {new Date(event.date).toLocaleDateString()}</p>
                            <p>Time: {event.time}</p>
                            <p>Audience: {event.audience_type}</p>
                            {event.room && (
                                <p>Location: {event.room.name} (Capacity: {event.room.capacity})</p>
                            )}
                        </div>
                        <button 
                            onClick={() => handleAttendEvent(event.event_id)}
                            disabled={event.attended}
                            className={event.attended ? 'attended' : ''}
                        >
                            {event.attended ? 'Attended' : 'Attend'}
                        </button>
                    </div>
                ))}
                
                {!loading && events.length === 0 && (
                    <p className="status-message">No events found matching your criteria.</p>
                )}
            </div>
        </div>
    );
}

export default Events;