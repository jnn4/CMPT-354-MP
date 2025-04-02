import '../app.css';
import React, {useEffect, useState} from 'react';

function personnel() {
    const [personnel, setPersonnel] = useState([]);
    const [searchText, setSearchText] = useState('');

    // Fetch personnel from Flask API
    useEffect(() => {
        fetch("http://localhost:8000/staff/")
            .then((response) => response.json()) // Convert response to JSON
            .then((data) => setPersonnel(data)) // Store the data in state
            .catch((error) => console.error("Error:", error));
    }, []);

    // Function to add a personnel
    window.onload = function() {
        fetch('http://localhost:8000/staff/populate_staff', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => console.log("Personnel added:", data))
        .catch(error => console.error('Error:', error));
    }

    // Function to filter personnel based on search text
    const filteredPersonnel = personnel.filter(
        (person) =>
            person.name.toLowerCase().includes(searchText.toLowerCase()) ||
            person.position.toLowerCase().includes(searchText.toLowerCase())
    );

    return (
        <div className="content">
            <h1>List of Personnel</h1>
            <p>We are ready to help you! Please contact us if you need help <a href="/contact">here</a>.</p>


            <ul className="items">
                {filteredPersonnel.map((person) => (
                    <li className="items" key={person.id}>
                        {person.name} - {person.position}
                        <p>Email: {person.email}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default personnel;