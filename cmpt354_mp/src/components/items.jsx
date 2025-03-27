import React, { useEffect, useState } from 'react';
import '../app.css';

function Items() {
  const [books, setBooks] = useState([]);
  const [searchText, setSearchText] = useState('');

  // Fetch books from Flask API
  useEffect(() => {
    fetch("http://localhost:5000/api/books")
      .then((response) => response.json()) // Convert response to JSON
      .then((data) => setBooks(data)) // Store the data in state
      .catch((error) => console.error("Error:", error));
  }, []);

  return (
    <div className="content">
      <h1>Library Books</h1>
      <p>Labels</p>
      <button className="items">Name</button>
      <button className="items">Audience</button>
      <button className="items">Date</button>
      <button className="items">Time</button>
      <button className="items">Type</button>

      <br></br>

      <input
        className = "rounded-textbox"
        type="text"
        placeholder="Search"
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
      />
      <ul className="items">
        {books.map((book) => (
          <li className="items" key={book.id}>
            {book.title} by {book.author} ({book.year_published})
          </li>
        ))}
      </ul>
      
    </div>
  );
}

export default Items;
