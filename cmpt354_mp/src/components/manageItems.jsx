import '../App.css';
import React, { useState, useEffect } from 'react';

function ManageItems() {
    const [items, setItems] = useState([]);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    // Fetch items when component mounts
    useEffect(() => {
        fetchItems();
    }, []);

    const fetchItems = async () => {
        try {
            const response = await fetch('http://localhost:8000/items/');
            if (!response.ok) {
                throw new Error('Failed to fetch items');
            }
            const data = await response.json();
            setItems(data);
        } catch (error) {
            setError('Error loading items: ' + error.message);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm('Are you sure you want to delete this item?')) {
            return;
        }

        try {
            const response = await fetch(`http://localhost:8000/items/${id}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('Failed to delete item');
            }

            setSuccess('Item deleted successfully');
            fetchItems(); // Refresh the list
        } catch (error) {
            setError('Error deleting item: ' + error.message);
        }
    };

    return (
        <div className="content">
            <h1>Manage Items</h1>
            {error && <p className="error-message">{error}</p>}
            {success && <p className="success-message">{success}</p>}
            
            <div className="items-list">
                {items.map((item) => (
                    <div key={item.id} className="item-card">
                        <h3>{item.title}</h3>
                        <p>Author: {item.author}</p>
                        <p>Year Published: {item.year_published}</p>
                        <p>Status: {item.borrowed ? 'Borrowed' : 'Available'}</p>
                        <p>Type: {item.type}</p>
                        <button 
                            className="delete-button"
                            onClick={() => handleDelete(item.id)}
                        >
                            Delete
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ManageItems; 