import React, { useState, useEffect } from 'react';
import '../App.css';
import LogoutButton from './LogoutButton';
import Volunteer from "./Volunteer";


function UserHome() {
    const [userData, setUserData] = useState(null); // Stores user details
    const [borrowedItems, setBorrowedItems] = useState([]); // Stores borrowed items
    const [upcomingEvents, setUpcomingEvents] = useState([]); // Stores upcoming events
    const [volunteeringHistory, setVolunteeringHistory] = useState([]); // Stores volunteering history
    const [donatedItems, setDonatedItemsHistory] = useState([]); // Stores volunteering history
    const [helpRequests, setHelpRequests] = useState([]); // Stores help requests
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
                    setBorrowedItems(data.borrowedItems);
                    setUpcomingEvents(data.upcomingEvents);
                    setVolunteeringHistory(data.volunteeringHistory); // Set volunteering history
                    setDonatedItemsHistory(data.donatedItems); // Set donating history
                    setHelpRequests(data.helpRequests) // Set help request history
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

    // Handle return item action
    const handleReturnItem = async (itemId) => {
        try {
          const response = await fetch(`http://localhost:8000/items/return`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              item_id: itemId,
              user_email: localStorage.getItem('userEmail') // Get email from localStorage
            }),
          });
      
          const data = await response.json();
          
          if (response.ok) {
            console.log("Return successful:", data);
            // Update UI state here
          } else {
            alert(data.message || 'Return failed');
          }
        } catch (error) {
          console.error('Error returning item:', error);
          alert('An error occurred while returning the item.');
        }
      };      

    if (errorMessage) {
        return <div className="content"><h1>Error</h1><p>{errorMessage}</p></div>;
    }

    if (!userData) {
        return <div className="content"><h1>Loading...</h1></div>;
    }

    // HANDLING UN REGISTER!
    const handleUnregisterEvent = async (eventId) => {
        try {
        const response = await fetch('http://localhost:8000/events/unregister', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
            user_email: localStorage.getItem('userEmail'),
            event_id: eventId
            }),
        });
    
        const data = await response.json();
        if (response.ok) {
            // Remove unregistered event from state
            setUpcomingEvents(prev => prev.filter(event => event.id !== eventId));
            alert(data.message);
        } else {
            alert(data.message || 'Unregistration failed');
        }
        } catch (error) {
        console.error('Error unregistering:', error);
        alert('Error unregistering from event');
        }
    };
  
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
                
                // Store user data in localStorage
                localStorage.setItem('userEmail', data.email);
                localStorage.setItem('userFirstName', data.first_name);
                localStorage.setItem('userLastName', data.last_name);
                localStorage.setItem('userPhoneNum', data.phone_num);
                localStorage.setItem('userAge', data.age);
                
                window.location.href = '/userHome';
            } else {
                setErrorMessage(data.message || 'Invalid email or password');
            }
        } catch (error) {
            console.error('Login error:', error);
            setErrorMessage('Unable to connect to server. Please try again.');
        }
    };

    const handleStopVolunteering = async (entryId) => {
        try {
            const response = await fetch(`http://localhost:8000/volunteer/stop`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: userData.email })
            });

            const data = await response.json();
            if (response.ok) {
                alert(data.message);
                window.location.reload(); // Refresh dashboard after stopping volunteering
            } else {
                alert(data.message || 'Failed to stop volunteering.');
            }
        } catch (error) {
            console.error('Error stopping volunteering:', error);
            alert('An error occurred while stopping volunteering.');
        }
    };


    const handleStartVolunteering = async () => {
        try {
            const response = await fetch(`http://localhost:8000/volunteer/start`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: userData.email }) // Ensure email is passed correctly
            });
    
            const data = await response.json();
            if (response.ok) {
                alert(data.message);
                window.location.reload(); // Refresh dashboard after starting volunteering
            } else {
                alert(data.message || 'Failed to start volunteering.');
            }
        } catch (error) {
            console.error('Error starting volunteering:', error);
            alert('An error occurred while starting volunteering.');
        }
    };    
    
    return (
        <div className='content'>
            <h1>Hi {userData.firstName} {userData.lastName}</h1>
            <p>Email: {userData.email}</p>
            <p>Phone Number: {userData.phoneNum}</p>
            <p>Age: {userData.age}</p>
            
            <button className="userHome">View Borrowed Items</button>
            <button className="userHome">Upcoming Events</button>
            <button className="userHome">Volunteering Position</button>
    
            <div>
                <h2>Borrowed Items</h2>
                {borrowedItems.length > 0 ? (
                    <ul className="items">
                        {borrowedItems.map(item => (
                            <li key={item.id} className="items">
                                <strong>{item.title}</strong> by {item.author} - Status: {item.status}
                                <button 
                                    className="items" 
                                    onClick={() => handleReturnItem(item.id)}
                                >
                                    Return
                                </button>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>You have no borrowed items.</p>
                )}
            </div>
    
            <div>
                <h2>Upcoming Events</h2>
                    {upcomingEvents.length > 0 ? (
                        <ul className="events">
                        {upcomingEvents.map(event => (
                            <li key={event.id} className="events">
                            {event.name} on {new Date(event.date).toLocaleDateString()} at {event.time}
                            <button 
                                onClick={() => handleUnregisterEvent(event.id)}
                                className="unregister-btn"
                            >
                                Unregister
                            </button>
                            </li>
                        ))}
                        </ul>
                    ) : (
                        <p>No upcoming registered events.</p>
                    )}
            </div>

            <div className="donated-section">
                <h2>Donated Items</h2>
                {donatedItems.length > 0 ? (
                    <div className="donated-grid">
                        {donatedItems.map(item => (
                            <div key={item.item_id} className="donated-card">
                                <h3>{item.title}</h3>
                                <div className="donation-details">
                                    <p><strong>Author:</strong> {item.author}</p>
                                    <p><strong>Type:</strong> {item.type}</p>
                                    <p><strong>Donated On:</strong> {item.donation_date}</p>
                                    <p><strong>Arrival Date:</strong> {item.arrival_date}</p>
                                    <p><strong>Current Status:</strong> 
                                        <span className={`status-${item.current_status}`}>
                                            {item.current_status}
                                        </span>
                                    </p>
                                    <p><strong>Donation Status:</strong> 
                                        <span className={`status-${item.donation_status}`}>
                                            {item.donation_status}
                                        </span>
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <p className="no-donations">You haven't donated any items yet</p>
                )}
            </div>

            <div>
                <h2>Help Requests</h2>
                {helpRequests.length > 0 ? (
                <ul>
                    {helpRequests.map(req => (
                    <li key={req.id}>
                        <p>{req.request_text}</p>
                        <p>Status: {req.status}</p>
                        <p>Submitted on: {new Date(req.created_at).toLocaleDateString()}</p>
                    </li>
                    ))}
                </ul>
                ) : (
                <p>No help requests found.</p>
                )}
            </div>

            <div>
                <h2>Volunteering History</h2>
                {volunteeringHistory.length > 0 ? (
                    <ul className="volunteer-list">
                        {volunteeringHistory.map((entry, index) => (
                            <li key={index}>
                                {new Date(entry.start_date).toLocaleDateString()} - 
                                {entry.end_date 
                                    ? new Date(entry.end_date).toLocaleDateString()
                                    : 'Present'}
                                <button 
                                    onClick={() => handleStopVolunteering(entry.id)}
                                    disabled={!!entry.end_date} // Disable button for completed entries
                                >
                                    {entry.end_date ? 'Completed' : 'Stop Volunteering'}
                                </button>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No volunteering history found</p>
                )}
                {!volunteeringHistory.some(entry => entry.status === 'active') && (
                    <button 
                        onClick={() => handleStartVolunteering()}
                        className="start-volunteer"
                    >
                        Start Volunteering Today!
                    </button>
                )}
            </div>
    
            <LogoutButton />
        </div>
    );    
}

export default UserHome;