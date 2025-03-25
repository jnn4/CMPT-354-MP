import React, { useEffect, useState } from 'react';
import '../app.css';

function Items() {
  const [books, setBooks] = useState([]);

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
      <ul>
        {books.map((book) => (
          <li key={book.id}>
            {book.title} by {book.author} ({book.year_published})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Items;
