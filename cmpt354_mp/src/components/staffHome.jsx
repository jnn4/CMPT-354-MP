import React, { useEffect, useState } from 'react';
import '../App.css';

function StaffHome() {
    const [staff, setStaff] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        // Get staff from localStorage
        const userData = localStorage.getItem('loggedInUser');
        if (!userData) {
            setError('Please log in to view your dashboard');
            return;
        }

        try {
            const parsedUser = JSON.parse(userData);
            
            // Fetch staff dashboard data
            fetch(`http://localhost:8000/auth/dashboard/staff?email=${parsedUser.email}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch staff data');
                    }
                    return response.json();
                })
                .then(data => {
                    setStaff(data);
                })
                .catch(error => {
                    console.error('Error fetching staff data:', error);
                    setError('Failed to load staff data');
                });
        } catch (error) {
            console.error('Error parsing user data:', error);
            setError('Error loading staff data');
        }
    }, []);

    if (!staff) {
        return (
            <div className='content'>
                <h1>Error</h1>
                <p>{error}</p>
            </div>
        );
    }

    return (
        <div className='content'>
            <div className="staff-welcome">
                <h1>Welcome, {staff.first_name}!</h1>
                <p className="staff-role">Library Staff Member</p>
            </div>

            <div className="staff-info-section">
                <h2>Your Information</h2>
                <div className="info-card">
                    <p><strong>Name:</strong> {staff.first_name} {staff.last_name}</p>
                    <p><strong>Email:</strong> {staff.email}</p>
                    <p><strong>Position:</strong> {staff.position}</p>
                    <p><strong>Phone:</strong> {staff.phone_num || 'Not provided'}</p>
                </div>
            </div>

            <div className="quick-actions">
                <h2>Quick Actions</h2>
                <div className="action-buttons">
                    <a href="/manage-items" className="action-button">
                        <h3>Manage Items</h3>
                        <p>Add, edit, or remove library items</p>
                    </a>
                    <a href="/manage-events" className="action-button">
                        <h3>Manage Events</h3>
                        <p>Create and manage library events</p>
                    </a>
                    <a href="/manage-fines" className="action-button">
                        <h3>Manage Fines</h3>
                        <p>View and process overdue fines</p>
                    </a>
                    <a href="/manage-staff" className="action-button">
                        <h3>Manage Staff</h3>
                        <p>View and manage staff members</p>
                    </a>
                    <a href="/manage-volunteers" className="action-button">
                        <h3>Manage Volunteers</h3>
                        <p>Coordinate volunteer activities</p>
                    </a>
                </div>
            </div>
        </div>
    );
}

export default StaffHome; 