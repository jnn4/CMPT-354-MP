import '../App.css';
import React from 'react';

function login(){
    return (
        <div className="content">
            <h1>Login</h1>
            <div className="container">
                <div className="box">
                    <form>
                        <label>Username: </label>
                        <br></br>
                        <input type="text" className="rounded-textbox" id="username" name="username" required></input>
                        <br></br>
                        <br></br>
                        <label>Password: </label>
                        <br></br>
                        <input type="password" className="rounded-textbox" id="password" name="password" required></input>
                        <br></br>
                        <button type="submit">Login</button>
                    </form>
                    <p>Don't have an account? <a href="/signup">[Sign Up]</a></p>
                </div>
            </div>    
        </div>
    );
}
export default login;