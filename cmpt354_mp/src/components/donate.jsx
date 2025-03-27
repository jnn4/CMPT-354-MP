import '../App.css';
import React from 'react';

function Donate() {
    return (
        <div className="content">
            <h1>Donate an Item</h1>
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
                </div>
            </div> 
        </div>
    );
}

export default Donate;