import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Doctors = () => {
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDoctors = async () => {
      try {
        const response = await api.get('/doctors/'); // Calls your Python GET /doctors/
        setDoctors(response.data);
      } catch (err) {
        console.error("Failed to fetch doctors", err);
      } finally {
        setLoading(false);
      }
    };
    fetchDoctors();
  }, []);

  if (loading) return <p>Loading Doctors...</p>;

  return (
    <div>
      <h2 style={{ color: '#0369a1', marginBottom: '20px' }}>Available Doctors</h2>
      <table style={styles.table}>
        <thead>
          <tr style={styles.headerRow}>
            <th>ID</th>
            <th>Name</th>
            <th>Specialization</th>
            <th>Availability</th>
          </tr>
        </thead>
        <tbody>
          {doctors.map((doc) => (
            <tr key={doc.id} style={styles.row}>
              <td>{doc.id}</td>
              <td style={{ fontWeight: '600' }}>{doc.name}</td>
              <td>{doc.specialization}</td>
              <td>{doc.is_available ? '✅ Available' : '❌ Busy'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const styles = {
  container: { padding: '10px' },
  title: { color: '#075985', fontSize: '28px', fontWeight: 'bold', marginBottom: '30px', borderBottom: '2px solid #e0f2fe', paddingBottom: '10px' },
  table: { width: '100%', borderCollapse: 'separate', borderSpacing: '0 15px' }, // Spacious gaps
  th: { textAlign: 'left', padding: '12px 20px', color: '#64748b', fontSize: '14px', textTransform: 'uppercase', letterSpacing: '1px' },
  tr: { background: 'white', transition: 'transform 0.2s', boxShadow: '0 2px 4px rgba(0,0,0,0.02)' },
  td: { padding: '20px', borderBottom: '1px solid #f1f5f9', fontSize: '16px', color: '#334155' },
  statusBadge: { display: 'flex', alignItems: 'center', gap: '8px', fontWeight: '600' }
};
export default Doctors;