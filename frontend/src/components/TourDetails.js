import React, { useEffect, useState } from "react";
import { Button, TextField, MenuItem } from "@mui/material";
import { useParams, useNavigate } from "react-router-dom";
import { format } from 'date-fns'; // Import format from date-fns
import api, { MainUrl } from "../services/api";
import {
    FaCalendarAlt, FaMapMarkerAlt, FaClock, FaUsers, FaDollarSign,
    FaExclamationCircle, FaArrowDown, FaVolumeUp, FaHeart, FaCheckCircle, FaTimesCircle, FaListUl
} from 'react-icons/fa';
import ImageCatalog from "./ImageCatalog";
import TourDatePicker from "./booking/TourDatePicker"; // Importing the TourDatePicker component
import "./Details.css";

const TourDetails = () => {
    const { id } = useParams();
    const [tour, setTour] = useState(null);
    const [selectedOffer, setSelectedOffer] = useState(null);
    const [selectedTourDay, setSelectedTourDay] = useState(null);
    const [isFavorite, setIsFavorite] = useState(false);
    const [imageLinks, setImageLinks] = useState([]);
    const [quantity, setQuantity] = useState(1);
    const [totalPrice, setTotalPrice] = useState(0);
    const [availableDates, setAvailableDates] = useState([]);
    const navigate = useNavigate();

    const handleBooking = async () => {
        try {
            if (selectedTourDay) {
                if (selectedTourDay.stock >= quantity) {
                    const bookingResponse = await api.post("/api/bookingtour/", {
                        tourday_id: selectedTourDay.id,
                        quantity,
                    });
                    console.log("Booking successful:", bookingResponse.data);
                    navigate("/bookings/");
                    window.location.reload();
                } else {
                    console.log("Not enough stock available for the selected date.");
                }
            } else {
                console.log("Selected date is not available.");
            }
        } catch (error) {
            console.log(error);
        }
    };

    useEffect(() => {
        const fetchTour = async () => {
            try {
                const response = await api.get(`/api/tour/${id}/`);
                setTour(response.data);
                const links = response.data.catalogs.map(catalog => `${MainUrl}${catalog.image}`);
                setImageLinks(links);

                // Check if the tour is already a favorite
                const favoriteResponse = await api.get(`/api/favorite-tour/${id}/`);
                setIsFavorite(favoriteResponse.data.is_favorite);
            } catch (error) {
                console.error("Failed to fetch tour details", error);
            }
        };
        fetchTour();
    }, [id]);

    useEffect(() => {
        if (selectedOffer) {
            const fetchTourDays = async () => {
                try {
                    const response = await api.get(`/api/tourdays/${selectedOffer.id}/`);
                    const availableDates = response.data.map(day => ({
                        date: format(new Date(day.day), 'yyyy-MM-dd'),
                        ...day
                    }));
                    setAvailableDates(availableDates);
                } catch (error) {
                    console.error("Failed to fetch tour days", error);
                }
            };
            fetchTourDays();
        }
    }, [selectedOffer]);

    useEffect(() => {
        if (selectedTourDay) {
            const price = parseFloat(selectedTourDay.tour_offer.price);
            setTotalPrice(price * quantity);
        }
    }, [quantity, selectedTourDay]);

    const toggleFavorite = async () => {
        try {
            if (isFavorite) {
                await api.delete(`/api/favorite-tour/${id}/`);
            } else {
                await api.post(`/api/favorite-tour/${id}/`);
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

    const toggleItinerary = (index) => {
        const itineraryContent = document.querySelectorAll('.itinerary-content')[index];
        itineraryContent.classList.toggle('show');
    };

    const handleOfferChange = (event) => {
        const offerId = event.target.value;
        const offer = tour.offers.find(offer => offer.id === parseInt(offerId));
        setSelectedOffer(offer);
        setSelectedTourDay(null);  // Reset selected tour day when changing the offer
        setAvailableDates([]);  // Clear out previous tour days
    };

    const handleDateChange = (date) => {
        const tourDay = availableDates.find(day => day.date === date);
        setSelectedTourDay(tourDay);
        setQuantity(1); // Reset quantity when changing the tour day
    };

    if (!tour) return <div>Loading...</div>;

    return (
        <div className="details-box" style={{
            backgroundImage: `url(${MainUrl}/${tour.image})`,
        }}>
            <div className="gradient-overlay"></div>
            <div className="details-container">
                <div className="details-header">
                    <h1 className="details-title">{tour.title}</h1>
                    <FaHeart
                        className={`favorite-icon ${isFavorite ? 'favorite' : ''}`}
                        onClick={toggleFavorite}
                    />
                </div>
                <img
                    src={`${MainUrl}/${tour.image}`}
                    alt={tour.title}
                    className="details-image"
                />
                <hr />
                <ImageCatalog imageLinks={imageLinks} />
                <div className="booking-container">
                    <h2>Book This Tour</h2>
                    <TextField
                        select
                        label="Select Offer"
                        value={selectedOffer?.id || ''}
                        onChange={handleOfferChange}
                        fullWidth
                    >
                        <MenuItem value="">Select Offer</MenuItem>
                        {tour.offers.map(offer => (
                            <MenuItem key={offer.id} value={offer.id}>
                                {offer.title} - ${offer.price}
                            </MenuItem>
                        ))}
                    </TextField>
                    {selectedOffer && (
                        <TourDatePicker
                            availableTourDays={availableDates.map(date => date.date)}
                            onDateChange={handleDateChange}
                        />
                    )}
                    {selectedTourDay && (
                        <>
                            <TextField
                                type="number"
                                label="Quantity"
                                value={quantity}
                                onChange={(e) => setQuantity(Math.min(Math.max(parseInt(e.target.value, 10), 1), selectedTourDay.stock))}
                                InputProps={{ inputProps: { min: 1, max: selectedTourDay.stock } }}
                                fullWidth
                                margin="normal"
                            />
                            <p><strong>Total Price:</strong> ${totalPrice.toFixed(2)}</p>
                            <Button
                                onClick={handleBooking}
                                variant="contained"
                                sx={{
                                    backgroundColor: "#1781a1",
                                    color: "#fff",
                                    "&:hover": {
                                        backgroundColor: "#ff7a2d",
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
                        {tour.description}
                    </p>
                    <p>
                        <FaDollarSign className="icon" /> <strong>Price:</strong> {tour.price}
                    </p>
                    <div className="date-info">
                        <p>
                            <FaCalendarAlt className="icon" /> <strong>Available from:</strong> {tour.available_from}
                        </p>
                        <p>
                            <FaCalendarAlt className="icon" /> <strong>to:</strong> {tour.available_to}
                        </p>
                    </div>
                    <p>
                        <FaClock className="icon" /> <strong>Duration:</strong> {tour.period} hours
                    </p>
                    <p className="map-container">
                        <FaMapMarkerAlt className="icon" /> <strong>Pickup location:</strong>
                        <div
                            className="map-container"
                            style={{
                                borderLeft: "6px solid orange"
                            }}
                            dangerouslySetInnerHTML={{ __html: tour.pickup_location }} />
                    </p>
                    <p>
                        <FaClock className="icon" /> <strong>Pickup time:</strong> {tour.pickup_time}
                    </p>
                    <p>
                        <FaClock className="icon" /> <strong>Dropoff time:</strong> {tour.dropoff_time}
                    </p>
                    <p>
                        <FaVolumeUp className="icon" /> <strong>Languages:</strong> {tour.languages}
                    </p>
                    <p>
                        <FaUsers className="icon" /> <strong>Minimum age:</strong> {tour.min_age}
                    </p>
                    <div className="included-excluded-container">
                        <div className="included-excluded-card">
                            <p><strong>Included:</strong></p>
                            <ul>
                                {tour.included_items.map(item => (
                                    <li key={item.id} className="included-item">
                                        <FaCheckCircle className="icon" /> {item.include}
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div className="included-excluded-card">
                            <p><strong>Not included:</strong></p>
                            <ul>
                                {tour.excluded_items.map(item => (
                                    <li key={item.id} className="excluded-item">
                                        <FaTimesCircle className="icon" /> {item.Exclude}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                    <p className="cancellation-policy">
                        <FaExclamationCircle className="icon" /> <strong>Cancellation policy:</strong> {tour.cancellation_policy}
                    </p>
                    <p>
                        <FaExclamationCircle className="icon" /> <strong>Additional info:</strong> {tour.additional_info}
                    </p>
                    <div className="itinerary-container">
                        <p className="itinerary-title">
                            Itinerary <FaListUl />
                        </p>
                        {tour.itinerary.map((step, index) => (
                            <div key={step.id} className="itinerary-step">
                                <p className="itinerary-step-title" onClick={() => toggleItinerary(index)}>
                                    {step.title} <FaArrowDown className="itinerary-arrow" />
                                </p>
                                <div className="itinerary-content">
                                    <p>{step.activity}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                    <div className="faq-container">
                        <p className="faq-title" onClick={toggleFaq}>
                            FAQs <FaArrowDown className="faq-arrow" />
                        </p>
                        <div className="faq-content">
                            {tour.faqs.map(faq => (
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

export default TourDetails;

