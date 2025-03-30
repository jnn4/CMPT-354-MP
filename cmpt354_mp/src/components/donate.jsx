import '../App.css';
import React, {useEffect, useState} from 'react';

function Donate() {
    const [title, setTitle] = useState('');
    const [author, setAuthor] = useState('');
    const [yearPublished, setYearPublished] = useState('');
    const [borrowed, setBorrowed] = useState(false);  // Initially, the book is not borrowed

    // Handle form submission
    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();  // Prevent default form submission behavior

        // Create the data object to send to the server
        const bookData = {
            title,
            author,
            year_published: yearPublished,
            borrowed,
        };

        try {
            // Send POST request to the backend API
            const response = await fetch('http://localhost:8000/api/books/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(bookData),
            });

            if (response.ok) {
                // Handle successful submission
                const result = await response.json();
                alert(result.message); // Display the response message from backend
            } else {
                // Handle error
                alert('Error adding book!');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('There was a problem with the request.');
        }
    };
    
    return (
        <div className="content">
            <h1>Donate an Item</h1>
            <div className="container">
                <div className="box">
                <form onSubmit={handleSubmit}>
                        {/* Title Input */}
                        <label>Title: </label>
                        <br />
                        <input
                            type="text"
                            className="rounded-textbox"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                        />
                        <br />
                        <br />
                        
                        {/* Author Input */}
                        <label>Author: </label>
                        <br />
                        <input
                            type="text"
                            className="rounded-textbox"
                            value={author}
                            onChange={(e) => setAuthor(e.target.value)}
                            required
                        />
                        <br />
                        <br />

                        {/* Year Published Input */}
                        <label>Publishing Year: </label>
                        <br />
                        <input
                            type="number"
                            className="rounded-textbox"
                            value={yearPublished}
                            onChange={(e) => setYearPublished(e.target.value)}
                            required
                        />
                        <br />
                        <br />

                        {/* Borrowed Radio Button */}
                        <label>Borrowed: </label>
                        <br />
                        <input
                            type="radio"
                            id="borrowedYes"
                            name="borrowed"
                            value="true"
                            checked={borrowed === true}
                            onChange={() => setBorrowed(true)}
                        />
                        <label htmlFor="borrowedYes">Yes</label>
                        <input
                            type="radio"
                            id="borrowedNo"
                            name="borrowed"
                            value="false"
                            checked={borrowed === false}
                            onChange={() => setBorrowed(false)}
                        />
                        <label htmlFor="borrowedNo">No</label>
                        <br />
                        <br />

                        {/* Submit Button */}
                        <button type="submit">Donate</button>
                    </form>
                </div>
            </div> 
        </div>
    );
}

export default Donate;