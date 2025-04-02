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
import UserHome from "./components/userHome";
import Events from "./components/events";
import Users from "./components/users";
import Rooms from "./components/rooms";
import ManageItems from "./components/manageItems";
import ManageEvents from "./components/manageEvents";
import ManageFines from "./components/manageFines";
import ManageStaff from './components/manageStaff';
import ManageVolunteers from './components/manageVolunteers';

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
            <Route path="/userHome" element={<UserHome />} />
            <Route path="/events" element={<Events />} />
            <Route path="/users" element={<Users />} />
            <Route path="/rooms" element={<Rooms />} />
            <Route path="/manage-items" element={<ManageItems />} />
            <Route path="/manage-events" element={<ManageEvents />} />
            <Route path="/manage-fines" element={<ManageFines />} />
            <Route path="/manage-staff" element={<ManageStaff />} />
            <Route path="/manage-volunteers" element={<ManageVolunteers />} />
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
