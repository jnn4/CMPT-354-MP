import React from 'react';
import '../App.css';
import { useEffect, useState } from 'react';

function events(){
    const [events, setEvents] = useState([]);
    const [searchText, setSearchText] = useState('');
    const [eventsPopulated, setEventsPopulated] = useState(false);

    // Fetch books from Flask API  
    useEffect(() => {
        fetch("http://localhost:8000/events/")
            .then((response) => response.json()) // Convert response to JSON
            .then((data) => setEvents(data)) // Store the data in state
            .catch((error) => console.error("Error:", error));
    }, []);

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

    const filteredEvents = events.filter((event) => {
        const title = event.title ? event.title.toLowerCase() : ""; 
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

            <p>Labels</p>
            <button className="items">Name</button>
            <button className="items">Audience</button>
            <button className="items">Date</button>
            <button className="items">Time</button>
            <button className="items">Type</button>

            <ul className="items">
                {filteredEvents.map((event, index) => (
                    <li className="items" key={event.id}>
                        {event.name}: {event.description} ({event.date}), room: {event.room_id}
                        {event.rsvp ? (
                            <button className="items">Attending</button>
                        ) : (
                            <button className="items">Available</button>
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