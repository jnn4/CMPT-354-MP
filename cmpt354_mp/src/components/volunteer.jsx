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
          <p>Have an account? <a href="/Login">[Log In]</a></p>
      </div>
      <div>
        <p>Available Position: </p>
        {/* Map positions that are left*/}
        <ul>
          <li>Position 1</li>
          <li>Position 2</li>
          <li>Position 3</li>
        </ul>
      </div>
    </div>
  );
}

export default volunteer;