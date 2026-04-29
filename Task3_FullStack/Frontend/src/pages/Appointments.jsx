import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Appointments = () => {
  const [doctors, setDoctors] = useState([]);
  const [patients, setPatients] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState('');
  const [selectedPat, setSelectedPat] = useState('');
  const [date, setDate] = useState('');
  const [msg, setMsg] = useState('');

  useEffect(() => {
    // Fetch both to fill the dropdowns
    api.get('/doctors/').then(res => setDoctors(res.data));
    api.get('/patients/').then(res => setPatients(res.data));
  }, []);

  const handleBook = async (e) => {
    e.preventDefault();
    setMsg("Booking...");

    if (!selectedDoc || !selectedPat || !date) {
        setMsg("❌ Please select all fields, bro.");
        return;
    }

    try {
      const payload = {
        doctor_id: Number(selectedDoc), // Use Number() to be safe
        patient_id: Number(selectedPat),
        appointment_date: date // Ensure this matches your Pydantic schema
      };

      await api.post('/appointments/', payload);
      setMsg("✅ Appointment booked! Check the Doctors tab now.");
    } catch (err) {
      console.error(err.response?.data); // CHECK THE CONSOLE FOR THE REAL ERROR
      setMsg(`❌ Error: ${err.response?.data?.detail || "Could not book"}`);
    }
  };
  
  return (
    <div>
      <h2 style={{ color: '#0369a1', marginBottom: '20px' }}>Book an Appointment</h2>
      {msg && <p style={{ padding: '10px', background: '#e0f2fe', borderRadius: '8px' }}>{msg}</p>}
      
      <form onSubmit={handleBook} style={styles.form}>
        <label>Select Doctor:</label>
        <select style={styles.input} onChange={(e) => setSelectedDoc(e.target.value)} required>
          <option value="">-- Choose Doctor --</option>
          {doctors.map(d => <option key={d.id} value={d.id}>{d.name} ({d.specialization})</option>)}
        </select>

        <label>Select Patient:</label>
        <select style={styles.input} onChange={(e) => setSelectedPat(e.target.value)} required>
          <option value="">-- Choose Patient --</option>
          {patients.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>

        <label>Date & Time:</label>
        <input type="datetime-local" style={styles.input} onChange={(e) => setDate(e.target.value)} required />

        <button type="submit" style={styles.button}>Confirm Booking</button>
      </form>
    </div>
  );
};

const styles = {
  form: { display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '400px' },
  input: { padding: '12px', borderRadius: '8px', border: '1px solid #bae6fd', outline: 'none' },
  button: { padding: '12px', background: '#0ea5e9', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold', marginTop: '10px' }
};

export default Appointments;


