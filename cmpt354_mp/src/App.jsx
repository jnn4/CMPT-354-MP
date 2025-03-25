import React from 'react';
import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/home";
import Items from "./components/items";
import Personnel from "./components/personnel";
import Volunteer from "./components/volunteer";
import Donate from "./components/donate";
import Contact from "./components/contact";
import Navbar from "./components/navbar";
import Login from "./components/login";
import Signup from "./components/signup";
import './app.css';

function App() {

  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <div className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/items" element={<Items />} />
            <Route path="/personnel" element={<Personnel />} />
            <Route path="/volunteer" element={<Volunteer />} />
            <Route path="/donate" element={<Donate />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
          </Routes>
          
          {/* Flask API Response */}
          {/* <div className="api-response">
            <h1>Flask + React (Vite JSX)</h1>
            <p>{data ? data : "Loading..."}</p>
          </div> */}
        </div>
      </div>
    </Router>
  );
}

export default App;
