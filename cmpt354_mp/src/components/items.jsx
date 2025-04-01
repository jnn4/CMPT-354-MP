import React, { useEffect, useState } from 'react';
import '../app.css';

function Items() {
  const [items, setItems] = useState([]);
  const [searchText, setSearchText] = useState('');
  const [itemsPopulated, setItemsPopulated] = useState(false);

  useEffect(() => {
    // Fetch books only once when the component mounts
    fetch("http://localhost:8000/items/")
      .then((response) => response.json())
      .then((data) => setItems(data))
      .catch((error) => console.error("Error fetching items:", error));
  }, []); // Empty dependency array ensures this only runs once after the component mounts

  // Function to populate books in the database (this will only run once, e.g., for testing)

const populateItems = () => {
  if (itemsPopulated) return; // Prevents re-population if already done

  fetch('http://localhost:8000/items/populate_items', {
    method: 'POST',
  })
    .then(response => response.json())
    .then(data => {
      console.log("Items populated:", data);
      setItemsPopulated(true);
    })
    .catch(error => console.error('Error populating items:', error));
};

  // Function to filter items based on search text
  const filteredItems = items.filter(
    (item) =>
      item.title.toLowerCase().includes(searchText.toLowerCase()) ||
      item.author.toLowerCase().includes(searchText.toLowerCase()) ||
      (item.year_published && item.year_published.toString().includes(searchText))
  );

  // Function that handles item borrowing
  const handleBorrowItem = (itemId) => {
    fetch(`http://localhost:8000/items/borrow/${itemId}`, { method: 'PATCH' })
      .then(response => response.json())
      .then(data => {
        if (data.message === "Item borrowed successfully") {
          // Update state to reflect borrowed item
          setItems(items.map(item =>
            item.id === itemId ? { ...item, borrowed: true } : item
          ));
        }
      })
      .catch(error => console.error('Error borrowing item:', error));
  };

  // Function that handles item return
  const handleReturnItem = (itemId) => {
    fetch(`http://localhost:8000/items/return/${itemId}`, { method: 'PATCH' })
      .then(response => response.json())
      .then(data => {
        if (data.message === "Item returned successfully") {
          // Update state to reflect returned item
          setItems(items.map(item =>
            item.id === itemId ? { ...item, borrowed: false } : item
          ));
        }
      })
      .catch(error => console.error('Error returning item:', error));
  };


  return (
    <div className="content">
      <h1>Library Books</h1>
      <p>Labels</p>
      <button className="items">Name</button>
      <button className="items">Audience</button>
      <button className="items">Date</button>
      <button className="items">Time</button>
      <button className="items">Type</button>

      <br />

      <input
        className="rounded-textbox"
        type="text"
        placeholder="Search"
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
      />

      <ul className="items">
      {filteredItems.map((item) => (
          <li className="items" key={item.id}>
            {item.title} by {item.author} ({item.year_published})
            {item.borrowed ? (
              <button className="items" onClick={() => handleReturnItem(item.id)}>
                Return
              </button>
            ) : (
              <button className="items" onClick={() => handleBorrowItem(item.id)}>
                Borrow
              </button>
            )}
          </li>
        ))}
        {filteredItems.length === 0 && searchText && (
          <li className="items">No results found</li>
        )}
      </ul>

      {/* Optional: Button to populate items (just for testing) */}
      <button onClick={populateItems} className="items">Populate Items</button>
    </div>
  );
}

export default Items;
