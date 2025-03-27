import '../app.css';
import React from 'react';

function personnel() {
    return (
        <div className="content">
            <h1>List of Personnel</h1>
            <p>We are ready to help you! Please contact us if you need help <a href="/contact">here</a>.</p>

            <ul className="items">
                <li className="items">
                    <h2>Camille</h2>
                    <p>Position: Manager</p>
                    <p>Email:</p>
                </li>
                <li className="items">
                    <h2>Camille</h2>
                    <p>Position: Manager</p>
                    <p>Email:</p>
                </li>
                <li className="items">
                    <h2>Camille</h2>
                    <p>Position: Manager</p>
                    <p>Email:</p>
                </li>
            </ul>
        </div>
    );
}

export default personnel;