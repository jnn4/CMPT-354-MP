import '../App.css';
import React, {useEffect, useState} from 'react';

function Donate() {
    const [formData, setFormData] = useState({
        title: '',
        author: '',
        type: 'book',
        pub_year: '',
        arrival_date: ''
    });

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

    return (
        <div className="content">
            <h1>Donate New Item</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Title"
                    required
                    onChange={e => setFormData({...formData, title: e.target.value})}
                />
                <input
                    type="text"
                    placeholder="Author"
                    required
                    onChange={e => setFormData({...formData, author: e.target.value})}
                />
                <select 
                    value={formData.type} 
                    onChange={e => setFormData({...formData, type: e.target.value})}
                >
                    <option value="book">Book</option>
                    <option value="magazine">Magazine</option>
                    <option value="cd">CD</option>
                </select>
                <input
                    type="number"
                    placeholder="Publication Year"
                    onChange={e => setFormData({...formData, pub_year: e.target.value})}
                />
                <input
                    type="date"
                    required
                    onChange={e => setFormData({...formData, arrival_date: e.target.value})}
                />
                <button type="submit">Donate Item</button>
            </form>
        </div>
    );
}

export default Donate;