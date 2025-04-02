import '../App.css';
import React, {useEffect, useState} from 'react';

function Donate() {
    const [itemType, setItemType] = useState('book');
    const [title, setTitle] = useState('');
    const [author, setAuthor] = useState('');
    const [yearPublished, setYearPublished] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage('');
        setError('');

        // First create the Item
        const itemData = {
            title: title,
            author: author,
            pub_year: yearPublished ? parseInt(yearPublished) : null,
            status: 'available',
            type: itemType
        };

        try {
            // Create the Item first
            const itemResponse = await fetch('http://localhost:8000/items/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(itemData),
            });

            const itemResult = await itemResponse.json();

            if (!itemResponse.ok) {
                throw new Error(itemResult.message || 'Failed to create item');
            }

            const itemId = itemResult.item_id;

            // Then create the FutureItem
            const futureItemData = {
                item_id: itemId,
                arrival_date: new Date().toISOString().split('T')[0] // Today's date in YYYY-MM-DD format
            };

            const futureItemResponse = await fetch('http://localhost:8000/future_items/post', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(futureItemData),
            });

            const futureItemResult = await futureItemResponse.json();

            if (futureItemResponse.ok) {
                setMessage('Thank you for your donation! It will be reviewed by our staff.');
                // Clear the form
                setTitle('');
                setAuthor('');
                setYearPublished('');
            } else {
                setError(futureItemResult.message || 'Error submitting donation');
            }
        } catch (error) {
            console.error('Error:', error);
            setError(error.message || 'There was a problem with the request.');
        }
    };
    
    return (
        <div className="content">
            <h1>Donate an Item</h1>
            <div className="container">
                <div className="box">
                    <form onSubmit={handleSubmit}>
                        {/* Item Type Selection */}
                        <label>Item Type: </label>
                        <br />
                        <select 
                            className="rounded-textbox"
                            value={itemType}
                            onChange={(e) => setItemType(e.target.value)}
                            required
                        >
                            <option value="book">Book</option>
                            <option value="cd">CD</option>
                            <option value="magazine">Magazine</option>
                        </select>
                        <br />
                        <br />

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
                        
                        {/* Author/Artist Input */}
                        <label>{itemType === 'book' ? 'Author' : itemType === 'cd' ? 'Artist' : 'Publisher'}: </label>
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
                        <label>Year Published: </label>
                        <br />
                        <input
                            type="number"
                            className="rounded-textbox"
                            value={yearPublished}
                            onChange={(e) => setYearPublished(e.target.value)}
                            min="1900"
                            max={new Date().getFullYear()}
                            placeholder="Optional"
                        />
                        <br />
                        <br />

                        {/* Submit Button */}
                        <button type="submit" className="submit-button">Submit Donation</button>
                    </form>

                    {message && <div className="success-message">{message}</div>}
                    {error && <div className="error-message">{error}</div>}
                </div>
            </div> 
        </div>
    );
}

export default Donate;