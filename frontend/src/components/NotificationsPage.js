import React, { useEffect, useState } from 'react';
import { styled } from '@mui/system';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';
import api from '../services/api.js';
import {useNavigate} from "react-router-dom";

const NotificationPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
}));

const TimeText = styled(Typography)({
  fontSize: '0.8em',
  color: 'gray',
});

const NotificationsPage = () => {
  const [notifications, setNotifications] = useState([]);
  const navigate = useNavigate();

    const handleNotfClick = () =>{
        navigate("/bookings/")
    }
  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const response = await api.get('/api/notifications/');
        setNotifications(response.data);
      } catch (error) {
        console.error('Error fetching notifications:', error);
      }
    };

    fetchNotifications();
  }, []);

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom>
        Notifications
      </Typography>
      {notifications.map(notification => (
        <NotificationPaper key={notification.id} onClick={handleNotfClick}>
          <Typography variant="body1">{notification.message}</Typography>
          <TimeText variant="body2">{new Date(notification.created_at).toLocaleString()}</TimeText>
        </NotificationPaper>
      ))}
    </Container>
  );
};

export default NotificationsPage;
