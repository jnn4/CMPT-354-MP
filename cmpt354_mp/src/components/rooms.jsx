import '../app.css'
import React, { useEffect, useState } from 'react';

function Rooms() {
  const [rooms, setRooms] = useState([]);
  const [roomsPopulated, setRoomsPopulated] = useState(false);

  useEffect(() => {
    // Fetch rooms only once when the component mounts
    fetch("http://localhost:8000/rooms/")
      .then((response) => response.json())
      .then((data) => setRooms(data))
      .catch((error) => console.error("Error fetching rooms:", error));
  }, []); // Empty dependency array ensures this only runs once after the component mounts

  const populateRooms = () => {
    if (roomsPopulated) return; // Prevents re-population if already done

    fetch('http://localhost:8000/rooms/populate', {  // Ensure this endpoint is for rooms
      method: 'POST',
    })
      .then(response => response.json())
      .then(data => {
        console.log("Rooms populated:", data);
        setRoomsPopulated(true);
      })
      .catch(error => console.error('Error populating rooms:', error));
  };

  return (
    <div className="content">
      <h1>List of Rooms</h1>

      {/* Only show the button if rooms are not populated */}
      {!roomsPopulated && (
        <button onClick={populateRooms} className="items">
          Populate Rooms
        </button>
      )}

      {/* Display the list of rooms */}
      <ul>
        {rooms.map((room) => (
          <li key={room.room_id}>
            {room.name} - capacity: {room.capacity}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Rooms;
