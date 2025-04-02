import '../App.css';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Signup() {
    const [formData, setFormData] = useState({
        email: '',
        first_name: '',
        last_name: '',
        password: '',
        phone_num: '',
        age: '',
        role: 'user'
    });
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });
    
            const data = await response.json();
            
            if (response.status === 201) {
                console.log('Signup successful', data);
                navigate('/login');
            } else {
                setErrorMessage(data.message || 'Error during signup');
                console.error('Signup error:', data);
            }
        } catch (error) {
            console.error('Error during signup:', error);
            setErrorMessage('Unable to connect to the server. Please check if the backend is running.');
        }
    };

    return (
        <div className="content">
            <div className="container">
                <div className="form-wrapper">
                    <h1>Sign Up</h1>
                    <div className="box">
                        <form onSubmit={handleSubmit}>
                            <label>First Name: </label>
                            <input
                                type="text"
                                className="rounded-textbox"
                                id="first_name"
                                name="first_name"
                                value={formData.first_name}
                                onChange={handleChange}
                                required
                            />
                            <label>Last Name: </label>
                            <input
                                type="text"
                                className="rounded-textbox"
                                id="last_name"
                                name="last_name"
                                value={formData.last_name}
                                onChange={handleChange}
                                required
                            />
                            <label>Email: </label>
                            <input
                                type="email"
                                className="rounded-textbox"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                required
                            />
                            <label>Password: </label>
                            <input
                                type="password"
                                className="rounded-textbox"
                                id="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                required
                            />
                            <label>Phone Number: </label>
                            <input
                                type="tel"
                                className="rounded-textbox"
                                id="phone_num"
                                name="phone_num"
                                value={formData.phone_num}
                                onChange={handleChange}
                                placeholder="Optional"
                            />
                            <label>Age: </label>
                            <input
                                type="number"
                                className="rounded-textbox"
                                id="age"
                                name="age"
                                value={formData.age}
                                onChange={handleChange}
                                min="0"
                                placeholder="Optional"
                            />
                            <label>Role: </label>
                            <select
                                className="rounded-textbox"
                                value={formData.role}
                                onChange={handleChange}
                                name="role"
                            >
                                <option value="user">User</option>
                                <option value="staff">Staff</option>
                            </select>
                            <button type="submit">Sign Up</button>
                        </form>
                        {errorMessage && <p className="error-message">{errorMessage}</p>}
                        <p className="login-link">Already have an account? <a href="/login">Log In</a></p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Signup;
