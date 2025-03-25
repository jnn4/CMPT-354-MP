import '../app.css'
import React from 'react';

function home (){
    return (
        <div className ="content">
            <h1>Library</h1>
            <h1>Data Management System</h1>
            <p><a href="/login">[Login]</a></p>
            <p><a href="/signup">[Sign Up]</a></p>
        </div>
    );
}

export default home;