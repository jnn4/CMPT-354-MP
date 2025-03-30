import '../app.css';
import React, {useEffect, useState} from 'react';

function volunteer() {
  const [volunteer, setVolunteer] = useState([]);

  // Fetch volunteer from Flask API
  useEffect(() => {
      fetch("http://localhost:8000/api/volunteer")
          .then((response) => response.json()) // Convert response to JSON
          .then((data) => setVolunteer(data)) // Store the data in state
          .catch((error) => console.error("Error:", error));
  }, []);

  // Function to add a volunteer
  window.onload = function() {
      fetch('http://localhost:8000/api/volunteer/populate_volunteer', {
          method: 'POST',
      })
      .then(response => response.json())
      .then(data => console.log("Volunteer added:", data))
      .catch(error => console.error('Error:', error));
  }


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

        <ul className="items">
          {volunteer.map((volunteer) => (
            <li className="items" key={volunteer.id}>
               {volunteer.position}
               <button className="items">Sign Up</button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default volunteer;