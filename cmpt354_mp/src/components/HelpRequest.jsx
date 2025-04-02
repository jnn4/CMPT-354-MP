import React, { useState } from 'react';

function HelpRequest() {
    const [requestText, setRequestText] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:8000/requests_help/create', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_email: localStorage.getItem('userEmail'), // Ensure the user is logged in
                    request_text: requestText
                })
            });

            const data = await response.json();
            if (response.ok) {
                setSuccessMessage(data.message);
                setRequestText(''); // Clear the form after submission
            } else {
                setErrorMessage(data.message || 'Failed to submit help request.');
            }
        } catch (error) {
            console.error('Error submitting help request:', error);
            setErrorMessage('An error occurred while submitting the help request.');
        }
    };

    return (
        <div className="content">
            <h1>Submit a Help Request</h1>
            <form onSubmit={handleSubmit}>
                <textarea
                    placeholder="Describe your issue..."
                    value={requestText}
                    onChange={(e) => setRequestText(e.target.value)}
                    required
                ></textarea>
                <button type="submit">Submit Request</button>
            </form>
            {successMessage && <p className="success-message">{successMessage}</p>}
            {errorMessage && <p className="error-message">{errorMessage}</p>}
        </div>
    );
}

export default HelpRequest;
