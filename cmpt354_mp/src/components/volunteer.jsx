import '../app.css';
import React from 'react';

function volunteer() {
  return (
    <div className="content">
      <h1>Volunteer Sign Up</h1>
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
              <button type="submit">Sign Up</button>
          </form>
      </div>
      <div className="volContainer">
        <p>Available Position: </p>
        {/* Map positions that are left*/}
        <ul className="items">
          <li className="items">Position 1</li>
          <li className="items" >Position 2</li>
          <li className="items">Position 3</li>
        </ul>
      </div>
    </div>
  );
}

export default volunteer;