import '../App.css';
import React, { useState } from 'react';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                }),
            });

            const data = await response.json();
            
            if (response.ok) {
                console.log('Login successful', data);
                // Store user data and redirect
                localStorage.setItem('userEmail', email);
                localStorage.setItem('userRole', data.role);  // Assuming backend returns role
                window.location.href = data.role === 'staff' ? '/staff-dashboard' : '/user-dashboard';
            } else {
                setErrorMessage(data.message || 'Invalid email or password');
            }
        } catch (error) {
            console.error('Login error:', error);
            setErrorMessage('Unable to connect to server. Please try again.');
        }
    };

    return (
        <div className="content">
            <h1>Login</h1>
            <div className="container">
                <div className="box">
                    <form onSubmit={handleSubmit}>
                        <label>Email: </label>
                        <input
                            type="email"
                            className="rounded-textbox"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            autoComplete="username"
                        />
                        
                        <label>Password: </label>
                        <input
                            type="password"
                            className="rounded-textbox"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            autoComplete="current-password"
                        />
                        
                        <button type="submit">Login</button>
                    </form>
                    
                    {errorMessage && <p className="error-message">{errorMessage}</p>}
                    
                    <p>Don't have an account? <a href="/signup">[Sign Up]</a></p>
                </div>
            </div>
        </div>
    );
}

export default Login;
