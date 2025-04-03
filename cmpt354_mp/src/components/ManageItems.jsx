import React, { useEffect, useState } from 'react';
import '../App.css';

function ManageItems() {
    const [items, setItems] = useState([]);

    useEffect(() => {
        const fetchItems = async () => {
            const response = await fetch('http://localhost:8000/items');
            const data = await response.json();
            setItems(data);
        };

        fetchItems();
    }, []);

    const handleDeleteItem = async (itemId) => {
        try {
            const response = await fetch(`http://localhost:8000/items/delete/${itemId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                alert('Item deleted successfully!');
                setItems(items.filter(item => item.item_id !== itemId));
            } else {
                alert('Failed to delete item.');
            }
        } catch (error) {
            console.error('Error deleting item:', error);
            alert('An error occurred while deleting the item.');
        }
    };

    return (
        <div style={{
            padding: '20px',
            textAlign: 'center',
            maxWidth: '800px',  // Limit the width of the container
            margin: '0 auto',   // Center the container horizontally
            marginTop: '80px',  // Adjust the top margin to avoid overlapping the navbar
        }}>
            <h1 style={{ fontSize: '24px', marginBottom: '20px' }}>Items</h1>
            <ul id='item-list' style={{ listStyleType: 'none', padding: '0' }}>
                {items.map(item => (
                    <li 
                        key={item.item_id} 
                        style={{
                            marginBottom: '10px',
                            padding: '10px',
                            backgroundColor: '#f0f0f0',
                            borderRadius: '5px',
                            display: 'flex',
                            justifyContent: 'space-between',
                        }}
                    >
                        <span>{item.title} by {item.author} ({item.type})</span>
                        <button 
                            onClick={() => handleDeleteItem(item.item_id)}
                            style={{
                                backgroundColor: '#d9534f',
                                color: 'white',
                                border: 'none',
                                borderRadius: '5px',
                            }}
                        >
                            Delete
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );    
}

export default ManageItems;
