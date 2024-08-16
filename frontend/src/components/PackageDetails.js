import React, { useEffect, useState } from "react";
import { Button, TextField, MenuItem } from "@mui/material";
import { useParams, useNavigate } from "react-router-dom";
import api, { MainUrl } from "../services/api";
import {
    FaCalendarAlt, FaMapMarkerAlt, FaClock, FaUsers, FaDollarSign,
    FaExclamationCircle, FaArrowDown, FaVolumeUp, FaHeart, FaCheckCircle, FaTimesCircle, FaListUl
} from 'react-icons/fa';
import ImageCatalog from "./ImageCatalog";
import PackageDatePicker from "./booking/PackageDatePicker"; // Importing the PackageDatePicker component
import { format } from 'date-fns'; // Ensure the date-fns format is imported
import "./Details.css";

const PackageDetails = () => {
    const { id } = useParams();
    const [pkg, setPkg] = useState(null);
    const [selectedOffer, setSelectedOffer] = useState(null);
    const [selectedPackageDay, setSelectedPackageDay] = useState(null);
    const [isFavorite, setIsFavorite] = useState(false);
    const [imageLinks, setImageLinks] = useState([]);
    const [quantity, setQuantity] = useState(1);
    const [totalPrice, setTotalPrice] = useState(0);
    const [availableDates, setAvailableDates] = useState([]);
    const navigate = useNavigate();

    const handleBooking = async () => {
        try {
            if (selectedPackageDay) {
                if (selectedPackageDay.stock >= quantity) {
                    const bookingResponse = await api.post("/api/bookingpackage/", {
                        package_offer_id: selectedPackageDay.package_offer.id,
                        start_date: selectedPackageDay.day,
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
        const fetchPackage = async () => {
            try {
                const response = await api.get(`/api/package/${id}/`);
                setPkg(response.data);
                const links = response.data.catalogs.map(catalog => `${MainUrl}${catalog.image}`);
                setImageLinks(links);

                // Check if the package is already a favorite
                const favoriteResponse = await api.get(`/api/favorite-package/${id}/`);
                setIsFavorite(favoriteResponse.data.is_favorite);
            } catch (error) {
                console.error("Failed to fetch package details", error);
            }
        };
        fetchPackage();
    }, [id]);

    useEffect(() => {
        if (selectedOffer) {
            const fetchPackageDays = async () => {
                try {
                    const response = await api.get(`/api/packagedays/${selectedOffer.id}/`);
                    setAvailableDates(response.data); // Set the entire package days data
                } catch (error) {
                    console.error("Failed to fetch package days", error);
                }
            };
            fetchPackageDays();
        }
    }, [selectedOffer]);

    useEffect(() => {
        if (selectedPackageDay) {
            const price = parseFloat(selectedPackageDay.package_offer.price);
            setTotalPrice(price * quantity);
        }
    }, [quantity, selectedPackageDay]);

    const toggleFavorite = async () => {
        try {
            if (isFavorite) {
                await api.delete(`/api/favorite-package/${id}/`);
            } else {
                await api.post(`/api/favorite-package/${id}/`);
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
        const offer = pkg.offers.find(offer => offer.id === parseInt(offerId));
        setSelectedOffer(offer);
        setSelectedPackageDay(null);  // Reset selected package day when changing the offer
        setAvailableDates([]);  // Clear out previous package days
    };

    const handleDateChange = (date) => {
        const packageDay = availableDates.find(day => format(new Date(day.day), 'yyyy-MM-dd') === date);
        setSelectedPackageDay(packageDay);
        setQuantity(1); // Reset quantity when changing the package day
    };

    if (!pkg) return <div>Loading...</div>;

    return (
        <div className="details-box" style={{
            backgroundImage: `url(${MainUrl}/${pkg.image})`,
        }}>
            <div className="gradient-overlay"></div>
            <div className="details-container">
                <div className="details-header">
                    <h1 className="details-title">{pkg.title}</h1>
                    <FaHeart
                        className={`favorite-icon ${isFavorite ? 'favorite' : ''}`}
                        onClick={toggleFavorite}
                    />
                </div>
                <img
                    src={`${MainUrl}/${pkg.image}`}
                    alt={pkg.title}
                    className="details-image"
                />
                <hr />
                <ImageCatalog imageLinks={imageLinks} />
                <div className="booking-container">
                    <h2>Book This Package Now!</h2>
                    <TextField
                        select
                        label="Select Offer"
                        value={selectedOffer?.id || ''}
                        onChange={handleOfferChange}
                        fullWidth
                    >
                        <MenuItem value="">Select Offer</MenuItem>
                        {pkg.offers.map(offer => (
                            <MenuItem key={offer.id} value={offer.id}>
                                {offer.title} - ${offer.price}
                            </MenuItem>
                        ))}
                    </TextField>
                    {selectedOffer && (
                        <PackageDatePicker
                            availablePackageDays={availableDates.map(day => format(new Date(day.day), 'yyyy-MM-dd'))}
                            onDateChange={handleDateChange}
                        />
                    )}
                    {selectedPackageDay && selectedPackageDay.package_offer && (
                        <>
                            <TextField
                                type="number"
                                label="Quantity"
                                value={quantity}
                                onChange={(e) => setQuantity(Math.min(Math.max(parseInt(e.target.value, 10), 1), selectedPackageDay.stock))}
                                InputProps={{ inputProps: { min: 1, max: selectedPackageDay.stock } }}
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
                        {pkg.description}
                    </p>
                    <p>
                            <FaDollarSign className="icon" /> <strong>Starting Price:</strong> ${pkg.offers[0].price}
                    </p>
                    <div className="date-info">
                        <p>
                            <FaCalendarAlt className="icon" /> <strong>Available from:</strong> {pkg.available_from}
                        </p>
                        <p>
                            <FaCalendarAlt className="icon" /> <strong>to:</strong> {pkg.available_to}
                        </p>
                    </div>
                    <p>
                        <FaClock className="icon" /> <strong>Pickup time:</strong> {pkg.pickup_time}
                    </p>
                    <p>
                        <FaClock className="icon" /> <strong>Dropoff time:</strong> {pkg.dropoff_time}
                    </p>
                    <p>
                        <FaCalendarAlt className="icon" /> <strong>Period:</strong> {pkg.period} days and {pkg.period - 1} nights
                    </p>
                    <p className="map-container">
                        <FaMapMarkerAlt className="icon" /> <strong>Location:</strong>
                        <div
                            className="map-container"
                            style={{
                                borderLeft: "6px solid orange"
                            }}
                            dangerouslySetInnerHTML={{ __html: pkg.pickup_location }} />
                    </p>
                    <p>
                        <FaVolumeUp className="icon" /> <strong>Languages:</strong> {pkg.languages}
                    </p>
                    <p>
                        <FaUsers className="icon" /> <strong>Minimum age:</strong> {pkg.min_age}
                    </p>
                    <div className="included-excluded-container">
                        <div className="included-excluded-card">
                            <p><strong>Included:</strong></p>
                            <ul>
                                {pkg.included_items.map(item => (
                                    <li key={item.id} className="included-item">
                                        <FaCheckCircle className="icon" /> {item.include}
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div className="included-excluded-card">
                            <p><strong>Not included:</strong></p>
                            <ul>
                                {pkg.excluded_items.map(item => (
                                    <li key={item.id} className="excluded-item">
                                        <FaTimesCircle className="icon" /> {item.Exclude}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                    <p className="cancellation-policy">
                        <FaExclamationCircle className="icon" /> <strong>Cancellation policy:</strong> {pkg.cancellation_policy}
                    </p>
                    <p>
                        <FaExclamationCircle className="icon" /> <strong>Additional info:</strong> {pkg.additional_info}
                    </p>
                    <div className="itinerary-container">
                        <p className="itinerary-title">
                            Itinerary <FaListUl />
                        </p>
                        {pkg.itinerary.map((step, index) => (
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
                            {pkg.faqs.map(faq => (
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

export default PackageDetails;
