import React, { useState, useEffect } from 'react';
import { CircularProgress, Container, Grid, Typography, Card, CardContent, CardHeader, Button, Alert, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import api, { MainUrl } from '../services/api';
import {
  FaDollarSign,
  FaClock,
  FaCalendarAlt,
  FaCheck,
  FaTimes,
  FaUser,
  FaEnvelope,
  FaPhone,
  FaBookmark,
  FaBoxOpen,
  FaRoute,
} from 'react-icons/fa';
import './Booking.css';

const SupplierBookingPage = () => {
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);
    const [activityBookings, setActivityBookings] = useState([]);
    const [packageBookings, setPackageBookings] = useState([]);
    const [tourBookings, setTourBookings] = useState([]);
    const [dashboardData, setDashboardData] = useState(null);
    const [filter, setFilter] = useState('all');

    const fetchBookings = async () => {
        try {
            const activitiesResponse = await api.get('/api/supplier/bookings/');
            const packagesResponse = await api.get('/api/supplier/packagesb/');
            const toursResponse = await api.get('/api/supplier/toursb/');
            const dashboardResponse = await api.get('/api/supplier-dashboard');
            
            setActivityBookings(activitiesResponse.data);
            setPackageBookings(packagesResponse.data);
            setTourBookings(toursResponse.data);
            setDashboardData(dashboardResponse.data);
        } catch (err) {
            setError(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchBookings();
    }, []);

    const handleConfirm = async (type, bookingId) => {
        try {
            let endpoint = '';
            if (type === 'activity') {
                endpoint = `/api/supplier/bookings/${bookingId}/confirm/`;
            } else if (type === 'package') {
                endpoint = `/api/supplier/package/${bookingId}/confirm/`;
            } else if (type === 'tour') {
                endpoint = `/api/supplier/tour/${bookingId}/confirm/`;
            }
            await api.post(endpoint);
            await fetchBookings();
        } catch (err) {
            setError(err);
        }
    };

    const filterBookings = (bookings) => {
        if (filter === 'all') return bookings;
        return bookings.filter(booking => {
            if (filter === 'paid') return booking.paid;
            if (filter === 'unpaid') return !booking.paid;
            if (filter === 'confirmed') return booking.confirmed;
            if (filter === 'unconfirmed') return !booking.confirmed;
            return true;
        });
    };

    const renderBookingList = (bookings, type) => (
        <Grid container spacing={2}>
            {bookings.length > 0 ? filterBookings(bookings).map(booking => {
                // Safely access nested properties
                const imageUrl = booking.period?.activity_offer?.activity?.image || booking.tourday?.tour_offer?.tour?.image || booking.package_offer?.package?.image;
                const title = booking.period?.activity_offer?.activity?.title || booking.tourday?.tour_offer?.tour?.title || booking.package_offer?.package?.title || 'Booking';
                const price = booking.period?.activity_offer?.price || booking.tourday?.tour_offer?.price || booking.package_offer?.price || 0;
                const day = booking.period?.day || booking.tourday?.day || booking.start_date;
                const startTime = booking.period?.time_from || booking.tourday?.time_from || booking.start_date;
                const endTime = booking.period?.time_to || booking.tourday?.time_to || booking.end_date;
                const customerUsername = booking.customer?.user?.username;
                const customerEmail = booking.customer?.user?.email;
                const customerPhone = booking.customer?.user?.phone;

                return (
                    <Grid item xs={12} sm={6} md={4} key={booking.id}>
                        <Card className="booking-card">
                            {imageUrl && (
                                <img 
                                    src={`${MainUrl}/${imageUrl}`} 
                                    className="booking-image"
                                    alt="Booking"
                                />
                            )}
                            <CardContent className="booking-content">
                                <Typography variant="h5" component="h2" className="booking-info">
                                    {title}
                                </Typography>
                                <Typography variant="body2" className="booking-info">
                                    <FaDollarSign className="icon-inline" /> Price: ${price}
                                </Typography>
                                <Typography variant="body2" className="booking-info">
                                    <FaCalendarAlt className="icon-inline" /> Day: {day}
                                </Typography>
                                <Typography variant="body2" className="booking-info">
                                    <FaClock className="icon-inline" /> Starts at: {startTime}
                                </Typography>
                                <Typography variant="body2" className="booking-info">
                                    <FaClock className="icon-inline" /> Ends at: {endTime}
                                </Typography>
                                {customerUsername && (
                                    <Typography variant="body2" className="booking-info">
                                        <FaUser className="icon-inline" /> Customer: {customerUsername}
                                    </Typography>
                                )}
                                {customerEmail && (
                                    <Typography variant="body2" className="booking-info">
                                        <FaEnvelope className="icon-inline" /> Email: {customerEmail}
                                    </Typography>
                                )}
                                {customerPhone && (
                                    <Typography variant="body2" className="booking-info">
                                        <FaPhone className="icon-inline" /> Phone: {customerPhone}
                                    </Typography>
                                )}
                                {!booking.confirmed ? (
                                    <Button variant="contained" color="primary" onClick={() => handleConfirm(type, booking.id)}>
                                        Confirm
                                    </Button>
                                ) : (
                                    <Typography variant="body1" className="booking-status confirmed">
                                        <FaCheck className="icon-inline" /> Confirmed
                                    </Typography>
                                )}
                            </CardContent>
                        </Card>
                    </Grid>
                );
            }) : <Typography className="no-bookings">No bookings available</Typography>}
        </Grid>
    );

    if (loading) return <Container className="container"><CircularProgress /></Container>;
    if (error) return <Container className="container"><Alert severity="error">Error loading bookings: {error.message}</Alert></Container>;

    return (
        <Container className="container">
            <Typography variant="h4" component="h1" gutterBottom className="section-title">
                Supplier Dashboard
            </Typography>

            {/* Dashboard Summary Section */}
            {dashboardData && (
                <Grid container spacing={4}>
                    <Grid item xs={12} md={6}>
                        <Card className="summary-card">
                            <CardContent>
                                <Typography variant="h5" component="h2">
                                    <FaDollarSign className="icon-inline" /> Total Sales: ${dashboardData.total_sales}
                                </Typography>
                                <Typography variant="h5" component="h2">
                                    <FaCheck className="icon-inline" /> Confirmed Bookings: {dashboardData.confirmed_bookings}
                                </Typography>
                                <Typography variant="h5" component="h2">
                                    <FaCheck className="icon-inline" /> Confirmed This Month: {dashboardData.confirmed_bookings_this_month}
                                </Typography>
                                <Typography variant="h5" component="h2">
                                    <FaTimes className="icon-inline" /> Unconfirmed Bookings: {dashboardData.unconfirmed_bookings}
                                </Typography>
                                <Typography variant="h5" component="h2">
                                    <FaTimes className="icon-inline" /> Unconfirmed This Month: {dashboardData.unconfirmed_bookings_this_month}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>

                    <Grid item xs={12} md={6}>
                        <Card className="summary-card">
                            <CardContent>
                                <Typography variant="h5" component="h2">
                                    <FaUser className="icon-inline" /> Today's Customers:
                                </Typography>
                                {dashboardData.todays_customers.length > 0 ? (
                                    dashboardData.todays_customers.map((customer, index) => (
                                        <Typography key={index} variant="body1">
                                            {customer[0]} at {new Date(customer[1]).toLocaleTimeString()}
                                        </Typography>
                                    ))
                                ) : (
                                    <Typography variant="body1">No customers today.</Typography>
                                )}
                            </CardContent>
                        </Card>
                    </Grid>
                </Grid>
            )}

            {/* Bookings Section */}
            <FormControl variant="outlined" className="filter-control">
                <InputLabel>Filter</InputLabel>
                <Select
                    value={filter}
                    onChange={(e) => setFilter(e.target.value)}
                    label="Filter"
                >
                    <MenuItem value="all">All</MenuItem>
                    <MenuItem value="paid">Paid</MenuItem>
                    <MenuItem value="unpaid">Unpaid</MenuItem>
                    <MenuItem value="confirmed">Confirmed</MenuItem>
                    <MenuItem value="unconfirmed">Unconfirmed</MenuItem>
                </Select>
            </FormControl>
            <Grid container spacing={4} direction="column">
                <Grid item>
                    <Card className="booking-card">
                        <CardHeader title={<><FaBookmark className="icon-inline" /> Activity Bookings</>} />
                        <CardContent>
                            {renderBookingList(activityBookings, 'activity')}
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item>
                    <Card className="booking-card">
                        <CardHeader title={<><FaBoxOpen className="icon-inline" /> Package Bookings</>} />
                        <CardContent>
                            {renderBookingList(packageBookings, 'package')}
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item>
                    <Card className="booking-card">
                        <CardHeader title={<><FaRoute className="icon-inline" /> Tour Bookings</>} />
                        <CardContent>
                            {renderBookingList(tourBookings, 'tour')}
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Container>
    );
};

export default SupplierBookingPage;