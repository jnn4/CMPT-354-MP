import React, { useState, useEffect } from 'react';
import '../App.css';
import LogoutButton from './LogoutButton';


function StaffHome() {
    const [userData, setUserData] = useState(null); // Stores user details
    const [errorMessage, setErrorMessage] = useState(''); // Error handling

    // Fetch user data after component mounts
    useEffect(() => {
        const fetchUserData = async () => {
            try {
                // Retrieve user details from localStorage
                const email = localStorage.getItem('userEmail');
                const firstName = localStorage.getItem('userFirstName');
                const lastName = localStorage.getItem('userLastName');
                const phoneNum = localStorage.getItem('userPhoneNum');
                const age = localStorage.getItem('userAge');
                
                console.log("LocalStorage Data:", { email, firstName, lastName, phoneNum, age });
    
                if (!email || !firstName || !lastName) {
                    setErrorMessage('User not logged in.');
                    return;
                }
    
                // Populate userData state
                setUserData({
                    email,
                    firstName,
                    lastName,
                    phoneNum,
                    age
                });
    
                // Fetch additional data (borrowed items, events, volunteering position) from backend
                const response = await fetch(`http://localhost:8000/auth/dashboard?email=${email}`);
                const data = await response.json();
    
                if (response.ok) {
                    console.log("Dashboard Data:", data);
                } else {
                    setErrorMessage(data.message || 'Failed to fetch user data.');
                }
            } catch (error) {
                console.error('Error fetching user data:', error);
                setErrorMessage('An error occurred while fetching user data.');
            }
        };
    
        fetchUserData();
    }, []);    

    if (errorMessage) {
        return <div className="content"><h1>Error</h1><p>{errorMessage}</p></div>;
    }

    if (!userData) {
        return <div className="content"><h1>Loading...</h1></div>;
    }

    return (
        <div className='content'>
            <h1>Hi {userData.firstName} {userData.lastName}</h1>
            <p>Email: {userData.email}</p>
            <p>Phone Number: {userData.phoneNum}</p>
            <p>Age: {userData.age}</p>
            <p><small>Welcome to the Staff Dashboard.</small></p>
    
            <LogoutButton />
        </div>
    );    
}

export default StaffHome;