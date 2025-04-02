import React, { useState, useEffect } from 'react';
import '../App.css';

function ManageStaff() {
    const [staff, setStaff] = useState([]);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    useEffect(() => {
        fetchStaff();
    }, []);

    const fetchStaff = async () => {
        try {
            const response = await fetch('http://localhost:8000/staff/');
            if (!response.ok) {
                throw new Error('Failed to fetch staff data');
            }
            const data = await response.json();
            setStaff(data);
        } catch (err) {
            setError('Error loading staff data');
            console.error('Error:', err);
        }
    };

    const handleDelete = async (staffId) => {
        if (!window.confirm('Are you sure you want to delete this staff member?')) {
            return;
        }

        try {
            const response = await fetch(`http://localhost:8000/staff/staff/${staffId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('Failed to delete staff member');
            }

            setSuccess('Staff member deleted successfully');
            fetchStaff(); // Refresh the list
        } catch (err) {
            setError('Error deleting staff member');
            console.error('Error:', err);
        }
    };

    return (
        <div className="content">
            <h1>Manage Staff</h1>
            {error && <div className="error-message">{error}</div>}
            {success && <div className="success-message">{success}</div>}
            
            <div className="management-grid">
                {staff.map((member) => (
                    <div key={member.staff_id} className="management-card">
                        <h3>{member.first_name} {member.last_name}</h3>
                        <p><strong>Position:</strong> {member.position}</p>
                        <p><strong>Email:</strong> {member.email}</p>
                        <button 
                            className="delete-button"
                            onClick={() => handleDelete(member.staff_id)}
                        >
                            Delete
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ManageStaff; 