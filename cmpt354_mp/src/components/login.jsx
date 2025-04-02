import '../App.css';
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();

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
                    email: email,
                    password: password
                }),
            });

            const data = await response.json();
            
            if (response.status === 200) {
                console.log('Login successful', data);

                // Store user info in localStorage with role
                localStorage.setItem('loggedInUser', JSON.stringify({
                    user_id: data.user_id,
                    name: `${data.first_name} ${data.last_name}`,
                    email: data.email,
                    role: data.role
                }));
                
                // Navigate to home page
                navigate('/userHome');
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
            <div className="container">
                <div className="form-wrapper">
                    <h1>Login</h1>
                    <div className="box">
                        <form onSubmit={handleSubmit}>
                            <label>Email: </label>
                            <input
                                type="email"
                                className="rounded-textbox"
                                id="email"
                                name="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                            />
                            <label>Password: </label>
                            <input
                                type="password"
                                className="rounded-textbox"
                                id="password"
                                name="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                            <button type="submit">Login</button>
                        </form>
                        {errorMessage && <p className="error-message">{errorMessage}</p>}
                        <p className="login-link">Don't have an account? <a href="/signup">Sign Up</a></p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Login;
