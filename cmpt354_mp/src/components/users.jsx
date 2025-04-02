import '../app.css'
import React, { useEffect, useState } from 'react';

function Users() {
  const [persons, setPersons] = useState([]);
  const [searchPeople, setSearchPeople] = useState('');
  const [personsPopulated, setPersonsPopulated] = useState(false);

  // map rooms
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    // Fetch persons only once when the component mounts
    fetch("http://localhost:8000/person/")
      .then((response) => response.json())
      .then((data) => setPersons(data))
      .catch((error) => console.error("Error fetching persons:", error));
  }, []); // Empty dependency array ensures this only runs once after the component mounts

  const populatePerson = () => {
    if (personsPopulated) return; // Prevents re-population if already done

    fetch('http://localhost:8000/person/populate', {
      method: 'POST',
    })
      .then(response => response.json())
      .then(data => {
        console.log("Persons populated:", data);
        setPersonsPopulated(true);
      })
      .catch(error => console.error('Error populating persons:', error));
  };
  


  return (
    <div className="content">
      <p>All persons</p>
      <input
        className="rounded-textbox"
        type="text"
        placeholder="Search"
        value={searchPeople}
        onChange={(e) => setSearchPeople(e.target.value)} // Update searchPeople state here
      />
      <button onClick={populatePerson} className="items">Populate Persons</button>
      <ul>
        {persons.map((person) => (
          <li key={person.email}>
            {person.firstName}, 
            {person.lastName}, 
            {person.email}, 
            {person.phoneNum}, 
            {person.age}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Users;
