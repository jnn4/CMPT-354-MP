import React from 'react';

function LogoutButton() {
    const handleLogout = () => {
        // Clear localStorage
        localStorage.removeItem('userEmail');
        localStorage.removeItem('userFirstName');
        localStorage.removeItem('userLastName');
        localStorage.removeItem('userPhoneNum');
        localStorage.removeItem('userAge');
        localStorage.removeItem('userRole');

        // Redirect to login page
        window.location.href = '/login';
    };

    return (
        <button onClick={handleLogout} className="logout-btn">
            Logout
        </button>
    );
}

export default LogoutButton;
