import React from 'react';

function Volunteer({ isVolunteering }) {
    const email = localStorage.getItem('userEmail');

    const handleVolunteer = async () => {
        try {
            const endpoint = isVolunteering ? '/volunteer/stop' : '/volunteer/start';
            const response = await fetch(`http://localhost:8000${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });

            const data = await response.json();
            if (response.ok) {
                window.location.reload(); // Refresh dashboard data
            }
            alert(data.message);
        } catch (error) {
            console.error('Volunteer action failed:', error);
            alert('Failed to update volunteer status');
        }
    };

    return (
        <button 
            onClick={handleVolunteer}
            className={`volunteer-btn ${isVolunteering ? 'stop' : 'start'}`}
        >
            {isVolunteering ? 'Stop Volunteering' : 'Yes, I want to volunteer today!'}
        </button>
    );
}

export default Volunteer;
