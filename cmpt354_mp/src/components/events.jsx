import React from 'react';
import '../App.css';
import { useState } from 'react';

function events(){
    const [books, setBooks] = useState([]);
    const [searchText, setSearchText] = useState('');
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
                <li className="items">
                    Event Name
                    Date
                    Time
                    Location
                    <button className="items">RSVP</button>
                </li>
                <li className="items">
                    Event Name
                    Date
                    Time
                    Location
                    <button className="items">RSVP</button>
                </li>
                <li className="items">
                    Event Name
                    Date
                    Time
                    Location
                    <button className="items">RSVP</button>
                </li>
            </ul>
        </div>
    )
}

export default events;