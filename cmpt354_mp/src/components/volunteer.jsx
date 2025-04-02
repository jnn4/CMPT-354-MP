import '../app.css';
import React, {useEffect, useState} from 'react';

function volunteer() {
  const [volunteer, setVolunteer] = useState([]);
  const [volunteerPopulated, setVolunteerPopulated] = useState(false);

  // Fetch volunteer from Flask API
  useEffect(() => {
      fetch("http://localhost:8000/volunteer/")
          .then((response) => response.json()) // Convert response to JSON
          .then((data) => setVolunteer(data)) // Store the data in state
          .catch((error) => console.error("Error:", error));
  }, []);

  // // Function to add a volunteer
  // window.onload = function() {
  //     fetch('http://localhost:8000/api/volunteer/populate_volunteer', {
  //         method: 'POST',
  //     })
  //     .then(response => response.json())
  //     .then(data => console.log("Volunteer added:", data))
  //     .catch(error => console.error('Error:', error));
  // }

  const populateVolunteer = () => {
    if (volunteerPopulated) return; // Prevents re-population if already done

    fetch('http://localhost:8000/person/populate', {
      method: 'POST',
    })
      .then(response => response.json())
      .then(data => {
        console.log("Persons populated:", data);
        setVolunteerPopulated(true);
      })
      .catch(error => console.error('Error populating persons:', error));
  };


  return (
    <div className="content">
      <h1>Volunteer Sign Up</h1>
      <div className="box">
          <form>
              <label>First Name: </label>
              <br></br>
              <input type="text" className="rounded-textbox" id="firstName" name="firstName" required></input>
              <br></br>
              <br></br>
              <label>Last Name: </label>
              <br></br>
              <input type="text" className="rounded-textbox" id="lastName" name="lastName" required></input>
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
        <p>Current Volunteers: </p>

        <button onClick={populateVolunteer} className="items">Populate Volunteer</button>

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