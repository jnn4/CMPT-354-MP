import '../app.css';
import React, {useEffect, useState} from 'react';

function personnel() {
    const [staff, setStaff] = useState([]);
    const [searchText, setSearchText] = useState('');
    const [staffPopulated, setStaffPopulated] = useState(false);

    // Fetch personnel from Flask API
    useEffect(() => {
        fetch("http://localhost:8000/staff/")
            .then((response) => response.json()) // Convert response to JSON
            .then((data) => setStaff(data)) // Store the data in state
            .catch((error) => console.error("Error:", error));
    }, []);

    // // Function to add a personnel
    // window.onload = function() {
    //     fetch('http://localhost:8000/staff/populate_staff', {
    //         method: 'POST',
    //     })
    //     .then(response => response.json())
    //     .then(data => console.log("Personnel added:", data))
    //     .catch(error => console.error('Error:', error));
    // }

    // Populate Personale
    const populateStaff = () => {
        if (staffPopulated) return; // Prevent multiple calls
    
        fetch('http://localhost:8000/staff/populate_staff', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            console.log("Staff populated:", data);
            setStaffPopulated(true);
        })
        .catch(error => console.error('Error populating staff:', error));
    };
    

    // Function to filter personnel based on search text
    const filteredPersonnel = staff.filter(
        (person) =>
            person.email.toLowerCase().includes(searchText.toLowerCase()) ||
            person.first_name.toLowerCase().includes(searchText.toLowerCase()) ||
            person.last_name.toLowerCase().includes(searchText.toLowerCase()) ||
            person.position.toLowerCase().includes(searchText.toLowerCase())
    );

    return (
        <div className="content">
            <h1>List of Personnel</h1>
            <p>We are ready to help you! Please contact us if you need help <a href="/contact">here</a>.</p>
            <a href="/users">Users</a>

            <input
                className = "rounded-textbox"
                type="text"
                placeholder="Search"
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
            />

            <ul className="items">
                {filteredPersonnel.map((person) => (
                    <li className="items" key={person.id}>
                        {person.first_name}, {person.last_name} - {person.position},
                        <p>Email: {person.email}</p>
                    </li>
                ))}
            </ul>

            {/* Optional: Button to populate items (just for testing) */}
            <button onClick={populateStaff} className="items">Populate Staff</button>

        </div>
    );
}

export default personnel;