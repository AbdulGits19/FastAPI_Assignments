import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Patients = () => {
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    api.get('/patients/').then(res => setPatients(res.data)).catch(err => console.log(err));
  }, []);

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Patient Directory</h2>
      <table style={styles.table}>
        <thead>
          <tr>
            <th style={styles.th}>ID</th>
            <th style={styles.th}>Full Name</th>
            <th style={styles.th}>Age</th>
            <th style={styles.th}>Gender</th>
          </tr>
        </thead>
        <tbody>
          {patients.map(p => (
            <tr key={p.id} style={styles.tr}>
              <td style={{...styles.td, color: '#94a3b8'}}>#{p.id}</td>
              <td style={{...styles.td, fontWeight: 'bold'}}>{p.name}</td>
              <td style={styles.td}>{p.age} years</td>
              <td style={styles.td}>{p.gender}</td>
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
  table: { width: '100%', borderCollapse: 'separate', borderSpacing: '0 15px' },
  th: { textAlign: 'left', padding: '12px 20px', color: '#64748b', fontSize: '14px', textTransform: 'uppercase', letterSpacing: '1px' },
  tr: { background: 'white', boxShadow: '0 2px 8px rgba(0,0,0,0.04)', borderRadius: '12px' },
  td: { padding: '20px', fontSize: '16px', color: '#334155' }
};

export default Patients;