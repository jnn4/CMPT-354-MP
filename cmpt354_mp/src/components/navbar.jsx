import React, {useEffect, useState} from 'react';
import './navbar.css';

function navbar(){
    const [current, setCurrent] = useState('home');


    return(
        <div className="sidebar">
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/items">Items</a></li>
                <li><a href="/events">Events</a></li>
                <li><a href="/personnel">Personnel</a></li>
                <li><a href="/volunteer">Volunteer</a></li>
                <li><a href="/donate">Donate</a></li>
                <li><a href="/contact">Contact</a></li>
                <li>Log out</li>
            </ul>
        </div>
    );
}

export default navbar;