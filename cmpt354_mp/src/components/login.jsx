import '../App.css';
import React, { useState } from 'react';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    // Handle form submit
    const handleSubmit = async (event) => {
        event.preventDefault();  // Prevent form from refreshing the page
        try {
            // Send POST request to backend
            const response = await fetch('http://localhost:8000/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: username,
                    password: password
                }),
            });

            const data = await response.json();
            
            if (response.status === 200) {
                console.log('Login successful', data);
                window.location.href = '/userHome';
            } else {
                // Show error message if login fails
                setErrorMessage(data.message || 'Invalid credentials');
            }
        } catch (error) {
            console.error('Error during login:', error);
            setErrorMessage('An error occurred during login. Please try again.');
        }
    };

    return (
        <div className="content">
            <h1>Login</h1>
            <div className="container">
                <div className="box">
                    <form onSubmit={handleSubmit}>
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
                        <button type="submit">Login</button>
                    </form>
                    {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
                    <p>Don't have an account? <a href="/signup">[Sign Up]</a></p>
                </div>
            </div>
        </div>
    );
}

export default Login;
