import '../App.css';
import React, { useState, useEffect } from 'react';

function ManageFines() {
    const [fines, setFines] = useState([]);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    // Fetch fines when component mounts
    useEffect(() => {
        fetchFines();
    }, []);

    const fetchFines = async () => {
        try {
            const response = await fetch('http://localhost:8000/fines/');
            if (!response.ok) {
                throw new Error('Failed to fetch fines');
            }
            const data = await response.json();
            setFines(data);
        } catch (error) {
            setError('Error loading fines: ' + error.message);
        }
    };

    const handleDelete = async (fineId) => {
        if (!window.confirm('Are you sure you want to delete this fine?')) {
            return;
        }

        try {
            const response = await fetch(`http://localhost:8000/fines/${fineId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('Failed to delete fine');
            }

            setSuccess('Fine deleted successfully');
            fetchFines(); // Refresh the list
        } catch (error) {
            setError('Error deleting fine: ' + error.message);
        }
    };

    return (
        <div className="content">
            <h1>Manage Fines</h1>
            {error && <p className="error-message">{error}</p>}
            {success && <p className="success-message">{success}</p>}
            
            <div className="fines-list">
                {fines.map((fine) => (
                    <div key={fine.fine_id} className="fine-card">
                        <h3>Fine ID: {fine.fine_id}</h3>
                        <p>Transaction ID: {fine.trans_id}</p>
                        <p>Amount: ${fine.fine_amount}</p>
                        <button 
                            className="delete-button"
                            onClick={() => handleDelete(fine.fine_id)}
                        >
                            Delete
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ManageFines; 