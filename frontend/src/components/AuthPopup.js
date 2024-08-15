import React, { useState, useEffect } from 'react';
import {
  Button,
  TextField,
  Box,
  Typography,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from '@mui/material';
import api from '../services/api.js';

const AuthPopup = () => {

  const handleLogin = async (username, password) => {
    try {
      const response = await api.post('/users/login/', { username, password });
      const { token } = response.data;
      localStorage.setItem('token', token);
      if (response.data.user.is_supplier) localStorage.setItem('s', response.data.user.is_supplier);
      localStorage.setItem('username', username);
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const handleRegister = async (username, email, password, phone) => {
    try {
      const response = await api.post('/users/register/', {
        username,
        email,
        password,
        phone,
      });
      const { token } = response.data;
      localStorage.setItem('token', token);
      localStorage.setItem('username', username);
      return response.data;
    } catch (error) {
      console.error('Register error:', error);
      throw error;
    }
  };

  const validatePassword = (password) => {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    if (password.length < minLength) {
      return 'Password must be at least 8 characters long';
    }
    if (!hasUpperCase) {
      return 'Password must contain at least one uppercase letter';
    }
    if (!hasLowerCase) {
      return 'Password must contain at least one lowercase letter';
    }
    if (!hasNumber) {
      return 'Password must contain at least one number';
    }
    if (!hasSpecialChar) {
      return 'Password must contain at least one special character';
    }
    return null;
  };

  const [open, setOpen] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [error, setError] = useState('');
  const [loggedInUser, setLoggedInUser] = useState(null);

  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      setLoggedInUser(storedUsername);
    }
  }, []);

  const handleClickOpen = () => setOpen(true);
  const handleClose = () => {
    setOpen(false);
    setError('');
  };
  const toggleAuthMode = () => setIsLogin(!isLogin);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    try {
      if (isLogin) {
        await handleLogin(username, password);
        window.location.reload(); // Refresh page on successful login
        setLoggedInUser(username);
      } else {
        const passwordError = validatePassword(password);
        if (passwordError) {
          setError(passwordError);
          return;
        }
        await handleRegister(name, email, password, phone);
        window.location.reload(); // Refresh page on successful registration
        setLoggedInUser(name);
      }
      handleClose();
    } catch (error) {
      const errorMessage = error.response?.data?.non_field_errors?.[0] || 'An error occurred. Please try again.';
      setError(errorMessage);
    }
  };


  return (
    <div>
      {loggedInUser ? (
        <Typography variant="h6">Hello, {loggedInUser}</Typography>
      ) : (
        <Button variant="contained" color="primary" onClick={handleClickOpen}>
          Login / Register
        </Button>
      )}
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>{isLogin ? 'Login' : 'Register'}</DialogTitle>
        <DialogContent>
          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
            {error && (
              <Typography color="error" sx={{ mb: 2 }}>
                {error}
              </Typography>
            )}
            {isLogin ? (
              <>
                <TextField
                  autoFocus
                  margin="dense"
                  id="username"
                  label="Username"
                  type="text"
                  fullWidth
                  variant="outlined"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
                <TextField
                  margin="dense"
                  id="password"
                  label="Password"
                  type="password"
                  fullWidth
                  variant="outlined"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </>
            ) : (
              <>
                <TextField
                  autoFocus
                  margin="dense"
                  id="name"
                  label="Name"
                  type="text"
                  fullWidth
                  variant="outlined"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
                <TextField
                  margin="dense"
                  id="email"
                  label="Email Address"
                  type="email"
                  fullWidth
                  variant="outlined"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
                <TextField
                  margin="dense"
                  id="password"
                  label="Password"
                  type="password"
                  fullWidth
                  variant="outlined"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                <TextField
                  margin="dense"
                  id="phone"
                  label="Phone Number"
                  type="text"
                  fullWidth
                  variant="outlined"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                />
              </>
            )}
            <DialogActions>
              <Button onClick={handleClose} color="secondary">
                Close
              </Button>
              <Button type="submit" color="primary">
                {isLogin ? 'Login' : 'Register'}
              </Button>
            </DialogActions>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={toggleAuthMode} color="primary">
            {isLogin ? 'Don\'t have an account? Register' : 'Already have an account? Login'}
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default AuthPopup;
