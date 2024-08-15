import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import api, { MainUrl } from "../services/api";
import "./Details.css";
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import CustomDatePicker from "./booking/CustomDatePicker";
import PeriodsDropdown from "./booking/PeriodsDropdown";
import MenuItem from '@mui/material/MenuItem';
import ImageCatalog from "./ImageCatalog";
import { FaCalendarAlt, FaMapMarkerAlt, FaClock, FaUsers, FaDollarSign, FaExclamationCircle, FaArrowDown, FaHeart, FaCheckCircle, FaTimesCircle } from 'react-icons/fa';

const ActivityDetails = () => {
    const { id } = useParams();
    const [activity, setActivity] = useState(null);
    const [selectedDate, setSelectedDate] = useState(null);
    const [selectedPeriod, setSelectedPeriod] = useState(null);
    const [quantity, setQuantity] = useState(1);
    const [isFavorite, setIsFavorite] = useState(false);
    const [offers, setOffers] = useState([]);
    const [selectedOffer, setSelectedOffer] = useState(null);
    const [imageLinks, setImageLinks] = useState([]);
    const [totalPrice, setTotalPrice] = useState(0);
    const navigate = useNavigate();

    const handleBooking = async () => {
        try {
            const data = { period_id: selectedPeriod.id, quantity };
            const response = await api.post('/api/bookingactivity/', data);
            if (response.data) {
                navigate("/");
                window.location.reload();
            }
        } catch (error) {
            console.error("Error booking:", error);
            alert("Error booking");
        }
    };

    useEffect(() => {
        const fetchActivity = async () => {
            try {
                const response = await api.get(`/api/activity/${id}/`);
                setActivity(response.data);
                const links = response.data.catalogs.map(catalog => `${MainUrl}${catalog.image}`);
                setImageLinks(links);

                // Check if the activity is already a favorite
                const favoriteResponse = await api.get(`/api/favorite-activity/${id}/`);
                setIsFavorite(favoriteResponse.data.is_favorite);

                // Fetch offers for the activity
                const offersResponse = await api.get(`/api/activity/${id}/offers/`);
                setOffers(offersResponse.data);
            } catch (error) {
                console.error("Failed to fetch activity details", error);
            }
        };
        fetchActivity();
    }, [id]);

    useEffect(() => {
        if (selectedPeriod) {
            const price = parseFloat(selectedPeriod.activity_offer.price);
            setTotalPrice(price * quantity);
        }
    }, [quantity, selectedPeriod]);

    const toggleFavorite = async () => {
        try {
            if (isFavorite) {
                await api.delete(`/api/favorite-activity/${id}/`);
            } else {
                await api.post(`/api/favorite-activity/${id}/`);
            }
            setIsFavorite(!isFavorite);
        } catch (error) {
            console.error("Error toggling favorite status", error);
        }
    };

    const toggleFaq = () => {
        const faqContent = document.querySelector('.faq-content');
        faqContent.classList.toggle('show');
    };

    const handleOfferChange = (event) => {
        const offerId = event.target.value;
        const offer = offers.find(offer => offer.id === parseInt(offerId));
        setSelectedOffer(offer);
        setSelectedPeriod(null); // Reset selected period when changing the offer
    };

    if (!activity) return <div>Loading...</div>;

    return (
        <div className="details-box">
            <div className="background-blur" style={{
                backgroundImage: `url(${MainUrl}/${activity.image})`,
            }}>
                <div className="gradient-overlay"></div>
            </div>
            <div className="details-container">
                <div className="details-header">
                    <h1 className="details-title">{activity.title}</h1>
                    <FaHeart 
                        className={`favorite-icon ${isFavorite ? 'favorite' : ''}`} 
                        onClick={toggleFavorite} 
                    />
                </div>
                <img
                    src={`${MainUrl}/${activity.image}`}
                    alt={activity.title}
                    className="details-image"
                />
                <ImageCatalog imageLinks={imageLinks} />
                <div className="booking-container">
                    <h2 className="booking-form-title">Book This Activity Now!</h2>
                    <CustomDatePicker
                        from={new Date().toISOString().split('T')[0]}
                        to={activity.available_to}
                        daysOff={activity.days_off}
                        onDateChange={setSelectedDate}
                    />
                    {selectedDate && (
                        <>
                            <TextField
                                select
                                label="Select Offer"
                                value={selectedOffer?.id || ''}
                                onChange={handleOfferChange}
                                fullWidth
                            >
                                <MenuItem value="">Select Offer</MenuItem>
                                {offers.map(offer => (
                                    <MenuItem key={offer.id} value={offer.id}>
                                        {offer.title} - ${offer.price}
                                    </MenuItem>
                                ))}
                            </TextField>
                            {selectedOffer && (
                                <PeriodsDropdown
                                    selectedDate={selectedDate}
                                    offerId={selectedOffer.id}
                                    setSelectedPeriod={setSelectedPeriod}
                                    selectedPeriod={selectedPeriod}
                                />
                            )}
                        </>
                    )}
                    {selectedPeriod && (
                        <>
                            <TextField
                                label="Quantity"
                                type="number"
                                InputProps={{ inputProps: { min: 1, max: selectedPeriod.stock } }}
                                value={quantity}
                                onChange={(e) => setQuantity(Math.max(1, Math.min(selectedPeriod.stock, Number(e.target.value))))}
                                variant="outlined"
                                margin="normal"
                            />
                            <p><strong>Total Price:</strong> ${(totalPrice).toFixed(2)}</p>
                            <Button
                                onClick={handleBooking}
                                variant="contained"
                                sx={{
                                    backgroundColor: '#1781a1',
                                    color: '#fff',
                                    '&:hover': {
                                        backgroundColor: '#ff7a2d',
                                    },
                                }}
                            >
                                BOOK NOW
                            </Button>
                        </>
                    )}
                </div>
                <div className="details-content">    
                    <p className="description">
                        <FaExclamationCircle className="icon" /> {activity.description}
                    </p>
                    <p>
                        <FaDollarSign className="icon" /> <strong>Price:</strong> {activity.price}
                    </p>
                    <div className="date-info">
                        <p>
                            <FaCalendarAlt className="icon" /> <strong>Available from:</strong> {activity.available_from}
                        </p>
                        <p>
                            <FaCalendarAlt className="icon" /> <strong>to:</strong> {activity.available_to}
                        </p>
                    </div>
                    <p>
                        <FaMapMarkerAlt className="icon" /> <strong>Location:</strong> {activity.location.name}
                    </p>
                    <p>
                        <FaClock className="icon" /> <strong>Start time:</strong> {activity.start_time}
                    </p>
                    <p>
                        <FaClock className="icon" /> <strong>End time:</strong> {activity.end_time}
                    </p>
                    <div className="included-excluded-container">
                        <div className="included-excluded-card">
                            <p><strong>Included:</strong></p>
                            <ul>
                                {activity.included_items.map(item => (
                                    <li key={item.id} className="included-item">
                                        <FaCheckCircle className="icon" /> {item.include}
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div className="included-excluded-card">
                            <p><strong>Not included:</strong></p>
                            <ul>
                                {activity.excluded_items.map(item => (
                                    <li key={item.id} className="excluded-item">
                                        <FaTimesCircle className="icon" /> {item.Exclude}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                    <p className="map-container">
                        <FaMapMarkerAlt color="orange" /> <strong>Activity location:</strong>
                        <div
                            style={{
                                borderLeft: "6px solid orange",
                            }}
                            dangerouslySetInnerHTML={{ __html: activity.map }} />
                    </p>
                    <p className="cancellation-policy">
                        <FaExclamationCircle className="icon" /> <strong>Cancellation policy:</strong> {activity.cancellation_policy}
                    </p>
                    <p>
                        <FaUsers className="icon" /> <strong>Group size:</strong> {activity.group_size}
                    </p>
                    <p>
                        <FaUsers className="icon" /> <strong>Participant age range:</strong> {activity.participant_age_range}
                    </p>
                    <div className="faq-container">
                        <p className="faq-title" onClick={toggleFaq}>
                            FAQs <FaArrowDown className="faq-arrow" />
                        </p>
                        <div className="faq-content">
                            {activity.faqs.map(faq => (
                                <div className="faq-item" key={faq.id}>
                                    <p><strong>Q:</strong> {faq.question}</p>
                                    <p><strong>A:</strong> {faq.answer}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ActivityDetails;

