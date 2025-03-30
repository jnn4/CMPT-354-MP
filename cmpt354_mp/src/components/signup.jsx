import '../App.css';
import React, { useState } from 'react';

function Signup() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [role, setRole] = useState('user');
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
                    email: username,
                    password: password,
                    name: name,
                    role: role
                }),
            });
    
            const data = await response.json();
            
            if (response.status === 200) {
                console.log('Signup successful', data);
                window.location.href = '/login';
            } else {
                setErrorMessage(data.message || 'Error during signup');
            }
        } catch (error) {
            console.error('Error during signup');
        }
    };

    return (
        <div className="content">
            <h1>Sign Up</h1>
            <div className="container">
                <div className="box">
                    <form onSubmit={handleSubmit}>
                        <label>Name: </label>
                        <br />
                        <input
                            type="text"
                            className="rounded-textbox"
                            id="name"
                            name="name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                        <br />
                        <br />
                        <label>Email: </label>
                        <br />
                        <input
                            type="text"
                            className="rounded-textbox"
                            id="username"
                            name="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                        <br />
                        <br />
                        <label>Password: </label>
                        <br />
                        <input
                            type="password"
                            className="rounded-textbox"
                            id="password"
                            name="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                        <br />
                        <br />
                        <label>Role: </label>
                        <br />
                        <select
                            value={role}
                            onChange={(e) => setRole(e.target.value)}
                        >
                            <option value="user">User</option>
                            <option value="admin">Admin</option>
                        </select>
                        <br />
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
