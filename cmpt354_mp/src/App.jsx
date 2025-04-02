import React from 'react';
import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/home";
import Items from "./components/items";
import Personnel from "./components/personnel";
import Volunteer from "./components/Volunteer";
import Donate from "./components/donate";
import HelpRequest from "./components/HelpRequest";
import Navbar from "./components/navbar";
import Login from "./components/login";
import Signup from "./components/signup";
import UserHome from "./components/userHome";
import Events from "./components/events";

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
            <Route path="/help-request" element={<HelpRequest />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/userHome" element={<UserHome />} />
            <Route path="/events" element={<Events />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
