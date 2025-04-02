import React, { useEffect, useState } from 'react';

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
        <div>
            <h1>Items</h1>
            <ul>
                {items.map(item => (
                    <li key={item.item_id}>
                        {item.title} by {item.author} ({item.type})
                        <button onClick={() => handleDeleteItem(item.item_id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ManageItems;
