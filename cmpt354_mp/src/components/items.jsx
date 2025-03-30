import React, { useEffect, useState } from 'react';
import '../app.css';

function Items() {
  const [books, setBooks] = useState([]);
  const [searchText, setSearchText] = useState('');

  useEffect(() => {
    // Fetch books only once when the component mounts
    fetch("http://localhost:8000/items/books")
      .then((response) => response.json())
      .then((data) => setBooks(data))
      .catch((error) => console.error("Error fetching books:", error));
  }, []); // Empty dependency array ensures this only runs once after the component mounts

  // Function to populate books in the database (this will only run once, e.g., for testing)
const [booksPopulated, setBooksPopulated] = useState(false);

const populateBooks = () => {
  if (booksPopulated) return; // Prevents re-population if already done

  fetch('http://localhost:8000/items/books/populate_books', {
    method: 'POST',
  })
    .then(response => response.json())
    .then(data => {
      console.log("Books populated:", data);
      setBooksPopulated(true);
    })
    .catch(error => console.error('Error populating books:', error));
};

  // Function to filter books based on search text
  const filteredBooks = books.filter(
    (book) =>
      book.title.toLowerCase().includes(searchText.toLowerCase()) ||
      book.author.toLowerCase().includes(searchText.toLowerCase()) ||
      (book.year_published && book.year_published.toString().includes(searchText))
  );

  // Function that handles book borrowing
  const handleBorrowBook = (bookId) => {
    fetch(`http://localhost:8000/items/books/borrow/${bookId}`, { method: 'PATCH' })
      .then(response => response.json())
      .then(data => {
        if (data.message === "Book borrowed successfully") {
          // Update state to reflect borrowed book
          setBooks(books.map(book =>
            book.id === bookId ? { ...book, borrowed: true } : book
          ));
        }
      })
      .catch(error => console.error('Error borrowing book:', error));
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
        {filteredBooks.map((book) => (
          <li className="items" key={book.id}>
            {book.title} by {book.author} ({book.year_published})
            {book.borrowed ? (
              <button className="items" disabled>
                Borrowed
              </button>
            ) : (
              <button className="items" onClick={() => handleBorrowBook(book.id)}>
                Available
              </button>
            )}
          </li>
        ))}
        {filteredBooks.length === 0 && searchText && (
          <li className="items">No results found</li>
        )}
      </ul>

      {/* Optional: Button to populate books (just for testing) */}
      <button onClick={populateBooks} className="items">Populate Books</button>
    </div>
  );
}

export default Items;
