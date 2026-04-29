import React, { useState } from 'react';
import api from '../services/api';

const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const formData = new URLSearchParams(); // Modern way to send form data
      formData.append('username', username);
      formData.append('password', password);

      console.log("Attempting login for:", username);
      
      const response = await api.post('/auth/login', formData);
      
      console.log("Backend Response:", response.data); // SEE WHAT PYTHON SENT BACK

      if (response.data.access_token) {
        localStorage.setItem('token', response.data.access_token);
        onLoginSuccess();
      } else {
        setError("Token not found in response.");
      }
    } catch (err) {
      console.error("Login Error Details:", err.response?.data || err.message);
      setError("Invalid credentials. Try again, bro.");
    }
  };
  
  return (
    <div style={styles.container}>
      <form onSubmit={handleLogin} style={styles.form}>
        <h2 style={styles.title}> Winterfell Hospitals </h2>
        <p style={styles.subtitle}>Medical Management Login Portal</p>
        
        {error && <p style={{color: '#c95555', fontSize: '13px'}}>{error}</p>}
        
        <input 
          type="text" 
          placeholder="Username" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
          style={styles.input}
          required
        />
        
        <div style={{height: '15px'}}></div>

        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          style={styles.input}
          required
        />
        
        <button type="submit" style={styles.button}>Enter Portal</button>
      </form>
    </div>
  );
};

const styles = {
  container: { 
    display: 'flex', 
    justifyContent: 'center', 
    alignItems: 'center', 
    height: '100vh',
    fontFamily: 'sans-serif'
  },
  form: { 
    padding: '40px', 
    background: 'rgba(255, 255, 255, 0.95)', 
    borderRadius: '24px', 
    boxShadow: '0 20px 40px rgba(2, 132, 199, 0.1)', 
    width: '360px',
    textAlign: 'center',
    border: '1px solid #e0f2fe'
  },
  title: {
    color: '#0369a1',
    marginBottom: '8px',
    fontSize: '28px',
    fontWeight: '800'
  },
  subtitle: {
    color: '#7dd3fc',
    marginBottom: '32px',
    fontSize: '14px',
    fontWeight: '500'
  },
  input: { 
    width: '100%', 
    padding: '14px 16px', 
    boxSizing: 'border-box', 
    border: '2px solid #f0f9ff', 
    borderRadius: '12px',
    backgroundColor: '#f8fafc',
    fontSize: '16px',
    color: '#0f172a',
    outline: 'none'
  },
  button: { 
    width: '100%', 
    padding: '14px', 
    background: 'linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%)', 
    color: 'white', 
    border: 'none', 
    borderRadius: '12px', 
    cursor: 'pointer',
    fontSize: '16px',
    fontWeight: '700',
    marginTop: '10px'
  }
};

export default Login;