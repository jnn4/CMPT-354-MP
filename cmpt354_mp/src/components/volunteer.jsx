import '../app.css';
import React, {useEffect, useState} from 'react';

function volunteer() {
  const [volunteers, setVolunteers] = useState([]);
  const [volunteerPopulated, setVolunteerPopulated] = useState(false);
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    role: '',
    availability: '',
    skills: ''
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  // Fetch volunteers from Flask API
  useEffect(() => {
    fetch("http://localhost:8000/volunteer/", {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    })
      .then((response) => response.json())
      .then((data) => setVolunteers(data))
      .catch((error) => console.error("Error:", error));
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');

    try {
      const response = await fetch('http://localhost:8000/volunteer/post', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          firstName: formData.firstName,
          lastName: formData.lastName,
          email: formData.email,
          phone: formData.phone,
          role: formData.role,
          availability: formData.availability,
          skills: formData.skills
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage('Successfully registered as a volunteer!');
        setFormData({
          firstName: '',
          lastName: '',
          email: '',
          phone: '',
          role: '',
          availability: '',
          skills: ''
        });
        // Refresh the volunteers list
        const updatedResponse = await fetch("http://localhost:8000/volunteer/", {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        });
        const updatedData = await updatedResponse.json();
        setVolunteers(updatedData);
      } else {
        setError(data.message || 'Failed to register as a volunteer');
      }
    } catch (err) {
      setError('Failed to connect to the server');
    }
  };

  const populateVolunteer = () => {
    if (volunteerPopulated) return;

    fetch('http://localhost:8000/volunteer/populate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        console.log("Volunteers populated:", data);
        setVolunteerPopulated(true);
        // Refresh the volunteers list after population
        return fetch("http://localhost:8000/volunteer/", {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        });
      })
      .then(response => response.json())
      .then(data => setVolunteers(data))
      .catch(error => console.error('Error populating volunteers:', error));
  };

  return (
    <div className="content">
      <h1>Volunteer Registration</h1>
      
      <div className="box">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>First Name: </label>
            <input 
              type="text" 
              className="rounded-textbox" 
              name="firstName" 
              value={formData.firstName}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Last Name: </label>
            <input 
              type="text" 
              className="rounded-textbox" 
              name="lastName" 
              value={formData.lastName}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Email: </label>
            <input 
              type="email" 
              className="rounded-textbox" 
              name="email" 
              value={formData.email}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Phone: </label>
            <input 
              type="tel" 
              className="rounded-textbox" 
              name="phone" 
              value={formData.phone}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Role: </label>
            <select 
              className="rounded-textbox" 
              name="role" 
              value={formData.role}
              onChange={handleInputChange}
              required
            >
              <option value="">Select a role</option>
              <option value="Event Coordinator">Event Coordinator</option>
              <option value="Mentor">Mentor</option>
              <option value="Workshop Leader">Workshop Leader</option>
              <option value="Admin Assistant">Admin Assistant</option>
              <option value="Marketing Assistant">Marketing Assistant</option>
            </select>
          </div>

          <div className="form-group">
            <label>Availability: </label>
            <textarea 
              className="rounded-textbox" 
              name="availability" 
              value={formData.availability}
              onChange={handleInputChange}
              placeholder="Please describe your availability"
              required
            />
          </div>

          <div className="form-group">
            <label>Skills: </label>
            <textarea 
              className="rounded-textbox" 
              name="skills" 
              value={formData.skills}
              onChange={handleInputChange}
              placeholder="Please list your relevant skills"
              required
            />
          </div>

          <button type="submit" className="submit-button">Register as Volunteer</button>
        </form>
      </div>

      {message && <div className="success-message">{message}</div>}
      {error && <div className="error-message">{error}</div>}

      </div>
  
  );
}

export default volunteer;