import React, { useEffect, useState } from 'react';
import '../App.css';

function Items() {
  const [items, setItems] = useState([]);
  const [searchText, setSearchText] = useState('');
  const [selectedType, setSelectedType] = useState('all');
  const [userEmail, setUserEmail] = useState('');

  // Get user email from localStorage on component mount
  useEffect(() => {
    const email = localStorage.getItem('userEmail');
    if (email) setUserEmail(email);
  }, []);

  // Fetch items and group by type
  useEffect(() => {
    fetch("http://localhost:8000/items")
      .then((response) => response.json())
      .then(data => {
        // Group items by type
        const grouped = data.reduce((acc, item) => {
          const type = item.type.toLowerCase();
          if (!acc[type]) acc[type] = [];
          acc[type].push(item);
          return acc;
        }, {});
        setItems(grouped);
      })
      .catch((error) => console.error("Error fetching items:", error));
  }, []);

  // --- HANDLE BORROW ITEM ---
  const handleBorrowItem = async (itemId) => {
    if (!userEmail) {
      alert('Please login to borrow items');
      return;
    }
  
    console.log("Borrowing Item:", { item_id: itemId, user_email: userEmail });
  
    try {
      const response = await fetch(`http://localhost:8000/items/borrow`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          item_id: parseInt(itemId), // Ensure it's a number
          user_email: userEmail.trim(), // Ensure no trailing spaces
        }),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        console.log("Borrow successful:", data);
        // Update UI state...
      } else {
        console.error("Borrow failed:", data.message);
        alert(data.message || 'Borrow failed');
      }
    } catch (error) {
      console.error('Error borrowing item:', error);
    }
  };
  

  const handleReturnItem = async (itemId) => {
    try {
      const response = await fetch(`http://localhost:8000/items/return`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          item_id: itemId,
          user_email: userEmail
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        // Update local state
        setItems(prev => ({
          ...prev,
          [data.item.type]: prev[data.item.type].map(item => 
            item.item_id === itemId ? data.item : item
          )
        }));
      } else {
        alert(data.message || 'Return failed');
      }
    } catch (error) {
      console.error('Error returning item:', error);
      alert('Error returning item');
    }
  };

  // Get filtered items based on search and type selection
  const filteredItems = Object.entries(items).reduce((acc, [type, items]) => {
    if (selectedType !== 'all' && selectedType !== type) return acc;
    
    const filtered = items.filter(item =>
      item.title.toLowerCase().includes(searchText.toLowerCase()) ||
      item.author.toLowerCase().includes(searchText.toLowerCase()) ||
      (item.pub_year && item.pub_year.toString().includes(searchText))
    );

    if (filtered.length > 0) acc[type] = filtered;
    return acc;
  }, {});

  return (
    <div className="content">
      <h1>Library Items</h1>
      
      <div className="filter-controls">
        <input
          className="rounded-textbox"
          type="text"
          placeholder="Search..."
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
        />
        
        <select 
          value={selectedType} 
          onChange={(e) => setSelectedType(e.target.value)}
        >
          <option value="all">All Types</option>
          {Object.keys(items).map(type => (
            <option key={type} value={type}>{type.charAt(0).toUpperCase() + type.slice(1)}</option>
          ))}
        </select>
      </div>

      {Object.entries(filteredItems).map(([type, items]) => (
        <div key={type} className="item-type-section">
          <h2>{type.charAt(0).toUpperCase() + type.slice(1)}</h2>
          <ul className="items-list">
            {items.map((item) => (
              <li key={item.item_id} className="item-card">
                <div className="item-info">
                  <h3>{item.title}</h3>
                  <p>Author: {item.author}</p>
                  <p>Year: {item.pub_year}</p>
                  <p>Status: {item.status}</p>
                </div>
                
                {item.status === "available" ? (
                  <button 
                    className="borrow-btn"
                    onClick={() => handleBorrowItem(item.item_id)}
                    disabled={!userEmail}
                  >
                    {userEmail ? 'Borrow' : 'Login to Borrow'}
                  </button>
                ) : (
                  item.status === "borrowed" && item.borrower_email === userEmail ? (
                    <button 
                      className="return-btn"
                      onClick={() => handleReturnItem(item.item_id)}
                    >
                      Return
                    </button>
                  ) : (
                    <span className="unavailable-text">Unavailable</span>
                  )
                )}
              </li>
            ))}
          </ul>
        </div>
      ))}

      {Object.keys(filteredItems).length === 0 && (
        <p className="no-results">No items found matching your criteria</p>
      )}
    </div>
  );
}

export default Items;