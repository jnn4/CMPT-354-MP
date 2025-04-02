import React, { useState, useEffect } from 'react';
import '../App.css';

function ManageVolunteers() {
    const [volunteers, setVolunteers] = useState([]);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    useEffect(() => {
        fetchVolunteers();
    }, []);

    const fetchVolunteers = async () => {
        try {
            const response = await fetch('http://localhost:8000/volunteer/');
            if (!response.ok) {
                throw new Error('Failed to fetch volunteers data');
            }
            const data = await response.json();
            setVolunteers(data);
        } catch (err) {
            setError('Error loading volunteers data');
            console.error('Error:', err);
        }
    };

    const handleDelete = async (volunteerId) => {
        if (!window.confirm('Are you sure you want to delete this volunteer?')) {
            return;
        }

        try {
            const response = await fetch(`http://localhost:8000/volunteer/${volunteerId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('Failed to delete volunteer');
            }

            setSuccess('Volunteer deleted successfully');
            fetchVolunteers(); // Refresh the list
        } catch (err) {
            setError('Error deleting volunteer');
            console.error('Error:', err);
        }
    };

    return (
        <div className="content">
            <h1>Manage Volunteers</h1>
            {error && <div className="error-message">{error}</div>}
            {success && <div className="success-message">{success}</div>}
            
            <div className="management-grid">
                {volunteers.map((volunteer) => (
                    <div key={volunteer.volunteer_id} className="management-card">
                        <h3>{volunteer.first_name} {volunteer.last_name}</h3>
                        <p><strong>Email:</strong> {volunteer.email}</p>
                        <p><strong>Phone:</strong> {volunteer.phone_num}</p>
                        <p><strong>Role:</strong> {volunteer.role}</p>
                        <p><strong>Start Date:</strong> {volunteer.start_date}</p>
                        <p><strong>End Date:</strong> {volunteer.end_date || 'Ongoing'}</p>
                        <button 
                            className="delete-button"
                            onClick={() => handleDelete(volunteer.volunteer_id)}
                        >
                            Delete
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ManageVolunteers; 