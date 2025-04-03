import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/home";
import Items from "./components/items";
import Donate from "./components/donate";
import HelpRequest from "./components/HelpRequest";
import Navbar from "./components/navbar";
import Login from "./components/login";
import Signup from "./components/signup";
import UserHome from "./components/userHome";
import StaffHome from "./components/staffHome";
import Events from "./components/events";
import ManageItems from './components/ManageItems';
import ManageEvents from './components/ManageEvents';
import ManageHelpRequest from './components/ManageHelpRequest';

function App() {

  return (
    <Router>
      <div className="app-container">
        <Navbar />
        <div className="content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/items" element={<Items />} />
            <Route path="/manage-items" element={<ManageItems />} />
            <Route path="/donate" element={<Donate />} />
            <Route path="/help-request" element={<HelpRequest />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/userHome" element={<UserHome />} />
            <Route path="/staffHome" element={<StaffHome />} />
            <Route path="/events" element={<Events />} />
            <Route path="/manage-events" element={<ManageEvents />} />
            <Route path="/manage-help-requests" element={<ManageHelpRequest />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
