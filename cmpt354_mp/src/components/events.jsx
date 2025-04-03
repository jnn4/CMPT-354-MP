import React from 'react';
import '../App.css';
import { useEffect, useState } from 'react';

function events(){
    const [events, setEvents] = useState([]);
    const [searchText, setSearchText] = useState('');
    const [eventsPopulated, setEventsPopulated] = useState(false);
    const [registeredEvents, setRegisteredEvents] = useState(new Set());
    const user = JSON.parse(localStorage.getItem('loggedInUser'));

    // Fetch events from Flask API  
    useEffect(() => {
        fetch("http://localhost:8000/events/")
            .then((response) => response.json())
            .then((data) => setEvents(data))
            .catch((error) => console.error("Error:", error));

        // Fetch user's registered events
        if (user) {
            fetch(`http://localhost:8000/events/user/${user.user_id}`)
                .then((response) => response.json())
                .then((data) => {
                    const registeredIds = new Set(data.map(event => event.event_id));
                    setRegisteredEvents(registeredIds);
                })
                .catch((error) => console.error("Error fetching registered events:", error));
        }
    }, [user]);

    // window.onload = function() {
    //     fetch('http://localhost:8000/events/populate_events', {
    //         method: 'POST',
    //     })
    //     .then(response => response.json())
    //     .then(data => console.log("Book added:", data))
    //     .catch(error => console.error('Error:', error));
    // };

    const populateEvents = () => {
        if (eventsPopulated) return; // Prevents re-population if already done

        fetch('http://localhost:8000/events/populate_events', {
            method: 'POST',
        })
            .then(response => response.json())
            .then(data => {
            console.log("Event populated:", data);
            setEventsPopulated(true);
            })
            .catch(error => console.error('Error populating event:', error));
    };

    const handleRegister = (eventId) => {
        if (!user) {
            alert('Please log in to register for events');
            return;
        }

        fetch(`http://localhost:8000/events/register/${eventId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: user.user_id })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            // Update registered events set
            setRegisteredEvents(prev => new Set([...prev, eventId]));
            alert('Successfully registered for event!');
        })
        .catch(error => {
            console.error('Error registering for event:', error);
            alert('Failed to register for event');
        });
    };

    const filteredEvents = events.filter((event) => {
        const title = event.name ? event.name.toLowerCase() : ""; 
        const description = event.description ? event.description.toLowerCase() : ""; 
        const eventDate = event.date ? event.date.toString() : ""; 
    
        return title.includes(searchText.toLowerCase()) ||
               description.includes(searchText.toLowerCase()) ||
               eventDate.includes(searchText);
    });

    return (
        <div className="content">
            <h1>Find Events in the Library</h1>
            <br></br>
            
            <input
                className = "rounded-textbox"
                type="text"
                placeholder="Search"
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
            />

            <br></br>
            <a href="/rooms">Rooms</a>

            <ul className="items">
                {filteredEvents.map((event, index) => (
                    <li className="items" key={event.event_id}>
                        {event.name}: {event.description} ({event.date}), room: {event.room_id}
                        {!user ? (
                            <button className="items" disabled style={{ opacity: 0.5, cursor: 'not-allowed' }}>
                                Register
                            </button>
                        ) : registeredEvents.has(event.event_id) ? (
                            <button className="items" disabled>Registered</button>
                        ) : (
                            <button 
                                className="items" 
                                onClick={() => handleRegister(event.event_id)}
                            >
                                Register
                            </button>
                        )}
                    </li>
                ))}
                {filteredEvents.length === 0 && searchText && (
                    <li className="items">No results found</li>
                )}
            </ul>

            {/* Optional: Button to populate items (just for testing) */}
            <button onClick={populateEvents} className="items">Populate Events</button>
        </div>
    )
}

export default events;