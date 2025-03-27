import '../app.css';
import React from 'react';

function contact() {
  return (
    <div className="content">
      <h1>Contact a Personnel</h1>
      <p>For any inquiries, please contact us at:</p>

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

export default contact;