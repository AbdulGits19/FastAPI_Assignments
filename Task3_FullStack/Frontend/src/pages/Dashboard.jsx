import React, { useState } from 'react';
import { Users, UserPlus, Calendar, LogOut } from 'lucide-react';
import Doctors from './Doctors'; 
import Patients from './Patients';
import Appointments from './Appointments';

const Dashboard = ({ onLogout }) => {
  const [activeTab, setActiveTab] = useState('doctors');

  const renderContent = () => {
    switch (activeTab) {
      case 'doctors': 
        return <Doctors />;
      case 'patients': 
        return <Patients />; // This now shows the real patient list
      case 'appointments': 
        return <Appointments />; 
      default: 
        return <Doctors />;
    }
  };

  return (
    <div style={styles.container}>
      <aside style={styles.sidebar}>
        <div style={styles.logo}> Winterfell Hospitals </div>
        <nav style={styles.nav}>
          <button onClick={() => setActiveTab('doctors')} style={activeTab === 'doctors' ? styles.activeBtn : styles.btn}>
            <Users size={20} /> Doctors
          </button>
          <button onClick={() => setActiveTab('patients')} style={activeTab === 'patients' ? styles.activeBtn : styles.btn}>
            <UserPlus size={20} /> Patients
          </button>
          <button onClick={() => setActiveTab('appointments')} style={activeTab === 'appointments' ? styles.activeBtn : styles.btn}>
            <Calendar size={20} /> Appointments
          </button>
        </nav>
        <button onClick={onLogout} style={styles.logoutBtn}>
          <LogOut size={20} /> Logout
        </button>
      </aside>
      <main style={styles.main}>
        
        <div style={styles.card}>{renderContent()}</div>
      </main>
    </div>
  );
};

const styles = {
  container: { display: 'flex', height: '100vh', background: '#f0f9ff' },
  sidebar: { width: '250px', background: '#075985', color: 'white', padding: '30px 20px', display: 'flex', flexDirection: 'column' },
  logo: { fontSize: '26px', fontWeight: '800', marginBottom: '40px', textAlign: 'center', color: '#e0f2fe' },
  nav: { flex: 1, display: 'flex', flexDirection: 'column', gap: '12px' },
  btn: { display: 'flex', alignItems: 'center', gap: '12px', padding: '14px', background: 'transparent', border: 'none', color: '#bae6fd', cursor: 'pointer', borderRadius: '12px', textAlign: 'left', fontSize: '16px' },
  activeBtn: { display: 'flex', alignItems: 'center', gap: '12px', padding: '14px', background: '#0ea5e9', border: 'none', color: 'white', cursor: 'pointer', borderRadius: '12px', textAlign: 'left', fontSize: '16px', fontWeight: 'bold' },
  logoutBtn: { display: 'flex', alignItems: 'center', gap: '12px', padding: '14px', background: 'rgba(239, 68, 68, 0.1)', border: 'none', color: '#fca5a5', cursor: 'pointer', borderRadius: '12px', marginTop: 'auto' },
  main: { flex: 1, padding: '40px', overflowY: 'auto' },
  card: { background: 'white', padding: '40px', borderRadius: '20px', minHeight: '80vh', boxShadow: '0 10px 25px rgba(0,0,0,0.02)' }
};

export default Dashboard;