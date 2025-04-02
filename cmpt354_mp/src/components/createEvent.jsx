import React, { useState, useEffect } from 'react';

function CreateEvent() {
    const [rooms, setRooms] = useState([]);
    const [formData, setFormData] = useState({
        name: '',
        type: '',
        date: '',
        time: '',
        room_id: '',
        min_age: '',
        max_age: '',
        audience_type: ''
    });

    useEffect(() => {
        // Fetch available rooms
        fetch('http://localhost:8000/rooms')
            .then(res => res.json())
            .then(data => setRooms(data))
            .catch(err => console.error('Error fetching rooms:', err));
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        try {
            const response = await fetch('http://localhost:8000/events/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            if (response.ok) {
                alert('Event created successfully!');
                setFormData({
                    name: '',
                    type: '',
                    date: '',
                    time: '',
                    room_id: '',
                    min_age: '',
                    max_age: '',
                    audience_type: ''
                });
            } else {
                alert(data.message || 'Failed to create event.');
            }
        } catch (err) {
            console.error('Error creating event:', err);
            alert('An error occurred.');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Event Name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
            />
            <select
                value={formData.room_id}
                onChange={(e) => setFormData({ ...formData, room_id: e.target.value })}
                required
            >
                <option value="">Select Room</option>
                {rooms.map(room => (
                    <option key={room.room_id} value={room.room_id}>
                        {room.name} (Capacity: {room.capacity})
                    </option>
                ))}
            </select>
            {/* Add other fields like type, date, time */}
            <button type="submit">Create Event</button>
        </form>
    );
}

export default CreateEvent;
