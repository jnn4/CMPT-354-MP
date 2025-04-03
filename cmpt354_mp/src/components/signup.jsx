import '../App.css';
import React, { useState } from 'react';

function Signup() {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        age: '',
        password: '',
        role: 'user'
    });
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    first_name: formData.firstName,
                    last_name: formData.lastName,
                    email: formData.email,
                    phone_num: formData.phone,
                    age: formData.age,
                    password: formData.password,  // Plaintext password sent here
                    role: formData.role,
                }),
            });
    
            const data = await response.json();
    
            if (response.status === 201) {
                console.log('Signup successful', data);
                window.location.href = '/login';
            } else {
                setErrorMessage(data.message || 'Error during signup');
            }
        } catch (error) {
            console.error('Error during signup:', error);
            setErrorMessage('Connection error. Please try again.');
        }
    };    

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    return (
        <div className="content">
            <h1>Sign Up</h1>
            <div className="container">
                <div className="box">
                    <form onSubmit={handleSubmit}>
                        <label>First Name: </label>
                        <input
                            type="text"
                            className="rounded-textbox"
                            name="firstName"
                            value={formData.firstName}
                            onChange={handleChange}
                            required
                        />
                        
                        <label>Last Name: </label>
                        <input
                            type="text"
                            className="rounded-textbox"
                            name="lastName"
                            value={formData.lastName}
                            onChange={handleChange}
                            required
                        />
                        
                        <label>Email: </label>
                        <input
                            type="email"
                            className="rounded-textbox"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                        />
                        
                        <label>Phone: </label>
                        <input
                            type="tel"
                            className="rounded-textbox"
                            name="phone"
                            value={formData.phone}
                            onChange={handleChange}
                            pattern="[0-9]{10}"
                        />
                        
                        <label>Age: </label>
                        <input
                            type="number"
                            className="rounded-textbox"
                            name="age"
                            value={formData.age}
                            onChange={handleChange}
                            min="1"
                        />
                        
                        <label>Password: </label>
                        <input
                            type="password"
                            className="rounded-textbox"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                        />
                        
                        <label>Role: </label>
                        <select
                            name="role"
                            value={formData.role}
                            onChange={handleChange}
                        >
                            <option value="user">User</option>
                            <option value="staff">Staff</option>
                        </select>
                        
                        <button type="submit">Sign Up</button>
                    </form>
                    {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
                    <p>Already have an account? <a href="/login">[Log In]</a></p>
                </div>
            </div>
        </div>
    );
}

export default Signup;
