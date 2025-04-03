import '../App.css';
import React, { useState } from 'react';

function Donate() {
    const [formData, setFormData] = useState({
        title: '',
        author: '',
        type: 'book',
        pub_year: '',
        arrival_date: ''
    });

    const [customTypes, setCustomTypes] = useState([]);  // New state to hold custom types
    const [newType, setNewType] = useState('');  // New state to capture the new type input

    // Handle the form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/donate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    ...formData,
                    user_email: localStorage.getItem('userEmail')
                })
            });
            
            const data = await response.json();
            if (response.ok) {
                alert('Donation successful!');
                window.location.href = '/userHome';
            } else {
                alert(data.error || 'Donation failed');
            }
        } catch (error) {
            console.error('Donation error:', error);
            alert('Connection error');
        }
    };

    // Handle adding a new custom type
    const handleAddType = () => {
        if (newType && !customTypes.includes(newType)) {
            setCustomTypes([...customTypes, newType]);
            setNewType('');
        } else {
            alert('Please enter a valid and unique type');
        }
    };

    return (
        <div style={{ padding: "8px", display: "flex", justifyContent: "center" }}>
        <div style={{ width: "100%", maxWidth: "280px" }}> {/* Max width added */}
            <h1 style={{ fontSize: "18px", marginBottom: "6px", textAlign: "center" }}>Donate</h1>
            <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "4px" }}>
                <input
                    type="text"
                    placeholder="Title"
                    required
                    onChange={e => setFormData({ ...formData, title: e.target.value })}
                    style={{ padding: "4px", border: "1px solid black", fontSize: "12px" }}
                />
                <input
                    type="text"
                    placeholder="Author"
                    required
                    onChange={e => setFormData({ ...formData, author: e.target.value })}
                    style={{ padding: "4px", border: "1px solid black", fontSize: "12px" }}
                />

                {/* Dropdown for selecting item type */}
                <div>
                    <select
                        value={formData.type}
                        onChange={e => setFormData({ ...formData, type: e.target.value })}
                        style={{ padding: "4px", border: "1px solid black", fontSize: "12px", width: "100%" }}
                    >
                        <option value="book">Book</option>
                        <option value="magazine">Magazine</option>
                        <option value="cd">CD</option>
                        <option value="journal">Journal</option>
                        <option value="record">Record</option>
                        {customTypes.map((type, index) => (
                            <option key={index} value={type}>{type}</option>
                        ))}
                    </select>
                </div>

                {/* Input for adding a new item type */}
                <div style={{ display: "flex", gap: "4px" }}>
                    <input
                        type="text"
                        value={newType}
                        placeholder="ex. Diary"
                        onChange={e => setNewType(e.target.value)}
                        style={{ padding: "4px", border: "1px solid black", fontSize: "12px", flex: 1 }}
                    />
                    <button 
                        type="button" 
                        onClick={handleAddType} 
                        style={{ padding: "4px", border: "1px solid black", fontSize: "12px" }}
                    >
                        Add a new Item Type
                    </button>
                </div>

                <input
                    type="number"
                    placeholder="Year"
                    onChange={e => setFormData({ ...formData, pub_year: e.target.value })}
                    style={{ padding: "4px", border: "1px solid black", fontSize: "12px" }}
                />
                <input
                    type="date"
                    required
                    onChange={e => setFormData({ ...formData, arrival_date: e.target.value })}
                    style={{ padding: "4px", border: "1px solid black", fontSize: "12px" }}
                />
                <button 
                    type="submit" 
                    style={{ padding: "4px", border: "1px solid black", fontSize: "12px" }}
                >
                    Donate
                </button>
            </form>
        </div>
    </div>

    );
}

export default Donate;
