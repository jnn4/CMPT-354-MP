import React from 'react';
import '../App.css';
import { useEffect, useState } from 'react';

function events(){
    const [events, setEvents] = useState([]);
    const [searchText, setSearchText] = useState('');

    // Fetch books from Flask API  
    useEffect(() => {
        fetch("http://localhost:8000/api/events")
            .then((response) => response.json()) // Convert response to JSON
            .then((data) => setEvents(data)) // Store the data in state
            .catch((error) => console.error("Error:", error));
    }, []);

    window.onload = function() {
        fetch('http://localhost:8000/api/events/populate_events', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => console.log("Book added:", data))
        .catch(error => console.error('Error:', error));
    };
    

    const filteredEvents = events.filter(
        (event) =>
            event.title.toLowerCase().includes(searchText.toLowerCase()) ||
            event.description.toLowerCase().includes(searchText.toLowerCase()) ||
            (event.date && event.date.toString().includes(searchText))
    );

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

            <p>Labels</p>
            <button className="items">Name</button>
            <button className="items">Audience</button>
            <button className="items">Date</button>
            <button className="items">Time</button>
            <button className="items">Type</button>

            <ul className="items">
                {filteredEvents.map((event) => (
                    <li className="items" key={event.id}>
                        {event.title} by {event.description} ({event.date})
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
        </div>
    )
}

export default events;