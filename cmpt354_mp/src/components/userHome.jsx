import React from 'react';
import '../App.css';

function userHome() {
    const user = JSON.parse(localStorage.getItem('loggedInUser'));

    console.log("Current User:", user.name);  // Display in console

    return (
        <div className='content'>
            <h1>Hi {user.name} </h1>
            <p>This is the user dashboard</p>
            <button className="userHome">View Borrowed Items</button>
            <button className="userHome">Upcoming Events</button>
            <button className="userHome">Volunteering position</button>

            <div>
                <h2>Borrowed Items</h2>
                <ul className="items">
                    <li className="items">
                        Item Name
                        Author
                        Status
                        <button className="items">Return</button>
                    </li>
                    <li className="items">
                        Item Name
                        Author
                        Status
                        <button className="items">Return</button>
                    </li>
                    <li className="items">
                        Item Name
                        Author
                        Status
                        <button className="items">Return</button>
                    </li>
                </ul>
            </div>

        </div>
    )
}

export default userHome;