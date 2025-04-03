import React, { useEffect, useState } from 'react';

function ManageHelpRequest() {
    const [helpRequests, setHelpRequests] = useState([]);

    useEffect(() => {
        const fetchHelpRequests = async () => {
            const response = await fetch('http://localhost:8000/requests_help');
            const data = await response.json();
            setHelpRequests(data);
        };

        fetchHelpRequests();
    }, []);

    const updateStatus = async (requestId, newStatus) => {
        try {
            const response = await fetch(`http://localhost:8000/requests_help/update/${requestId}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status: newStatus })
            });

            if (response.ok) {
                alert('Status updated successfully!');
                setHelpRequests(prev =>
                    prev.map(req =>
                        req.request_id === requestId ? { ...req, status: newStatus ? 'Open' : 'Closed' } : req
                    )
                );
            } else {
                alert('Failed to update status.');
            }
        } catch (error) {
            console.error('Error updating status:', error);
            alert('An error occurred while updating the status.');
        }
    };
    return (
        <div>
            <h2>Manage Help Requests</h2>
            {helpRequests.length > 0 ? (
                <ul>
                    {helpRequests.map(req => (
                        <li key={req.request_id} style={{ marginBottom: '5%' }}>
                            <strong>Description: </strong> {req.request_text}
                            <br></br>
                            <strong>Status: </strong> {req.status}
                            <br></br>
                            <button onClick={() => updateStatus(req.request_id, true)}>Mark as Open</button>
                            <button onClick={() => updateStatus(req.request_id, false)}>Mark as Closed</button>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No help requests found.</p>
            )}
        </div>
    );
}

export default ManageHelpRequest;