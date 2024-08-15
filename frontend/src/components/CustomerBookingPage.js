import React, { useState, useEffect } from 'react';
import {
  CircularProgress,
  Container,
  Grid,
  Typography,
  Card,
  CardContent,
  CardHeader,
  Alert
} from '@mui/material';
import {
  FaDollarSign,
  FaClock,
  FaCalendarAlt,
  FaShoppingCart,
  FaCheck,
  FaTimes,
  FaQrcode,
  FaBookmark,
  FaHistory,
  FaExclamationTriangle
} from 'react-icons/fa';
import api, { MainUrl } from '../services/api';
import './Booking.css';

const Bookings = () => {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activityBookings, setActivityBookings] = useState([]);
  const [packageBookings, setPackageBookings] = useState([]);
  const [tourBookings, setTourBookings] = useState([]);
  const today = new Date();

  const isBookingStillValid = (bookingDay) => {
    const bookingDate = new Date(bookingDay);
    return bookingDate >= today;
  };

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const activitiesResponse = await api.get('/api/customer/bookings/');
        const packagesResponse = await api.get('/api/customer/packagesb/');
        const toursResponse = await api.get('/api/customer/toursb/');

        setActivityBookings(activitiesResponse.data);
        setPackageBookings(packagesResponse.data);
        setTourBookings(toursResponse.data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchBookings();
  }, []);

  if (loading) return <Container className="container"><CircularProgress /></Container>;
  if (error) return <Container className="container"><Alert severity="error">Error loading bookings: {error.message}</Alert></Container>;

  const filterBookings = (bookings, getDate, getPaid, getConfirmed) => {
    const main = bookings.filter(booking => !getPaid(booking) && isBookingStillValid(getDate(booking)));
    const history = bookings.filter(booking => getConfirmed(booking) && getPaid(booking));
    const expired = bookings.filter(booking => !getConfirmed(booking) && !getPaid(booking) && !isBookingStillValid(getDate(booking)));
    return { main, history, expired };
  };

  const activityData = filterBookings(activityBookings, booking => booking.period.day, booking => booking.paid, booking => booking.confirmed);
  const packageData = filterBookings(packageBookings, booking => booking.end_date, booking => booking.paid, booking => booking.confirmed);
  const tourData = filterBookings(tourBookings, booking => booking.tourday.day, booking => booking.paid, booking => booking.confirmed);

  const combinedBookings = {
    main: [...activityData.main, ...packageData.main, ...tourData.main],
    history: [...activityData.history, ...packageData.history, ...tourData.history],
    expired: [...activityData.expired, ...packageData.expired, ...tourData.expired]
  };

  const renderBookingList = (bookings) => (
    <Grid container spacing={2}>
      {bookings.length > 0 ? bookings.map(booking => {
        // Extract necessary data with safe checks
        const activityImage = booking.period?.activity_offer?.activity?.image || '';
        const tourImage = booking.tourday?.tour_offer?.tour?.image || '';
        const packageImage = booking.package_offer?.package?.image || '';

        const title = booking.period?.activity_offer?.activity?.title ||
                      booking.tourday?.tour_offer?.tour?.title ||
                      booking.package_offer?.package?.title ||
                      'Booking';

        const unit = booking.period?.activity_offer?.activity?.unit ||
                     booking.tourday?.tour_offer?.tour?.unit ||
                     booking.package_offer?.package?.unit ||
                     'unit';

        const price = booking.period?.activity_offer?.price ||
                      booking.tourday?.tour_offer?.price ||
                      booking.package_offer?.price || 0;

        const day = booking.period?.day ||
                    booking.tourday?.day ||
                    booking.start_date;

        const startTime = booking.period?.time_from ||
                          booking.tourday?.time_from ||
                          booking.start_date;

        const endTime = booking.period?.time_to ||
                        booking.tourday?.time_to ||
                        booking.end_date;

        return (
          <Grid item xs={12} sm={6} md={4} key={booking.id}>
            <Card className="booking-card">
              <img 
                src={`${MainUrl}/${activityImage || tourImage || packageImage}`} 
                className="booking-image"
                alt="Booking"
              />
              <CardContent className="booking-content">
                <Typography variant="h5" component="h2" className="booking-info">
                  {title}
                </Typography>
                <Typography variant="body2" className="booking-info">
                  <FaDollarSign className="icon-inline" />
                  Price: ${price * booking.quantity}
                </Typography>
                <Typography variant="body2" className="booking-info">
                  <FaShoppingCart className="icon-inline" />
                  Quantity: {booking.quantity} {unit}
                </Typography>
                <Typography variant="body2" className="booking-info">
                  <FaCalendarAlt className="icon-inline" />
                  Day: {day}
                </Typography>
                <Typography variant="body2" className="booking-info">
                  <FaClock className="icon-inline" />
                  Starts at: {startTime}
                </Typography>
                <Typography variant="body2" className="booking-info">
                  <FaClock className="icon-inline" />
                  Ends at: {endTime}
                </Typography>
                <Typography variant="body1" className={`booking-status ${booking.paid ? 'paid' : 'unpaid'}`}>
                  {booking.paid ? <><FaCheck className="icon-inline" /> Paid</> : <><FaTimes className="icon-inline" /> Unpaid</>}
                </Typography>
                <Typography variant="body1" className={`booking-status ${booking.confirmed ? 'confirmed' : 'not-confirmed'}`}>
                  {booking.confirmed ? <><FaCheck className="icon-inline" /> Confirmed</> : <><FaTimes className="icon-inline" /> Not confirmed</>}
                </Typography>
                {booking.confirmed && booking.qr_code && (
                  <div>
                    <Typography variant="body2"><FaQrcode className="icon-inline" /> QR Code:</Typography>
                    <img src={`${MainUrl}${booking.qr_code}`} alt="QR Code" className="qr-code" />
                  </div>
                )}
              </CardContent>
            </Card>
          </Grid>
        );
      }) : <Typography className="no-bookings">No bookings available</Typography>}
    </Grid>
  );

  return (
    <Container className="container">
      <Grid container spacing={4} direction="column">
        <Grid item>
          <Card className="booking-card">
            <CardHeader title={<><FaBookmark className="icon-inline" /> Active Bookings</>} />
            <CardContent>
              {renderBookingList(combinedBookings.main)}
            </CardContent>
          </Card>
        </Grid>
        <Grid item>
          <Card className="booking-card">
            <CardHeader title={<><FaHistory className="icon-inline" /> History Bookings</>} />
            <CardContent>
              {renderBookingList(combinedBookings.history)}
            </CardContent>
          </Card>
        </Grid>
        <Grid item>
          <Card className="booking-card">
            <CardHeader title={<><FaExclamationTriangle className="icon-inline" /> Expired Bookings</>} />
            <CardContent>
              {renderBookingList(combinedBookings.expired)}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Bookings;
