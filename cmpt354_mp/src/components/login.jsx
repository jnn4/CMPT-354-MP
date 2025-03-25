import '../App.css';
import React from 'react';

function login(){
    return (
        <div className="content">
            <h1>Login</h1>
            <form>
                <label>Username: </label>
                <input type="text" id="username" name="username" required></input>
                <br></br>
                <label>Password: </label>
                <input type="password" id="password" name="password" required></input>
                <br></br>
                <button type="submit">Login</button>
            </form>
        </div>
    );
}
export default login;