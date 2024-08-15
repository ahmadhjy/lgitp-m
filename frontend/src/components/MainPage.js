import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import './MainPage.css';
import Card from './Card';
import { FaStar, FaClock, FaGift, FaHiking, FaMapSigns, FaBoxOpen, FaMap, FaBox, FaWalking } from 'react-icons/fa';

const MainPage = () => {
  const [loggedInUser, setLoggedInUser] = useState(null);

  const [activities, setActivities] = useState([]);
  const [tours, setTours] = useState([]);
  const [packages, setPackages] = useState([]);
  const [latestItems, setLatestItems] = useState([]);
  const [featuredItems, setFeaturedItems] = useState([]);
  const [forYouItems, setForYouItems] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      setLoggedInUser(storedUsername);
    }

    const fetchData = async () => {
      try {
        const [activitiesResponse, toursResponse, packagesResponse, latestResponse, featuredResponse] = await Promise.all([
          api.get('/api/activities/'),
          api.get('/api/tours/'),
          api.get('/api/packages/'),
          api.get('/api/latest/'),
          api.get('/api/featured-items/'),
        ]);

        setActivities(activitiesResponse.data);
        setTours(toursResponse.data);
        setPackages(packagesResponse.data);
        setLatestItems(latestResponse.data);
        setFeaturedItems(featuredResponse.data);
      } catch (error) {
        console.error('Failed to fetch data', error);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    if (loggedInUser) {
      const fetchForYouItems = async () => {
        try {
          const foryouResponse = await api.get('/api/for-you/');
          setForYouItems(foryouResponse.data);
        } catch (error) {
          console.error('Failed to fetch for you items', error);
        }
      };

      fetchForYouItems();
    }
  }, [loggedInUser]);

  const handleCardClick = (id, type) => {
    navigate(`/${type}-details/${id}`);
  };

  return (
    <div className="main-page">
      <div className="banner">
        <div className="banner-content">
          <div className="banner-text">Top Tips-Top Trips</div>
          <div className="banner-subtext">Welcome to LebAdvisor: Packages, Daily Tours & Activities</div>
          <div className="banner-buttons">
            <button className="banner-button" onClick={() => navigate('/all-tours/')}>
              <FaMap className="banner-button-icon" /> Tours
            </button>
            <button className="banner-button" onClick={() => navigate('/all-packages/')}>
              <FaBox className="banner-button-icon" /> Packages
            </button>
            <button className="banner-button" onClick={() => navigate('/all-activities/')}>
              <FaWalking className="banner-button-icon" /> Activities
            </button>
          </div>
        </div>
      </div>

      {loggedInUser && (
        <div className="section">
          <h1 className="section-title">Recommended</h1>
          <div className="scrollable-row">
            {forYouItems.activities?.map((activity) => (
              <Card key={activity.id} item={activity} onClick={() => handleCardClick(activity.id, 'activity')} />
            ))}
            {forYouItems.packages?.map((pkg) => (
              <Card key={pkg.id} item={pkg} onClick={() => handleCardClick(pkg.id, 'package')} />
            ))}
            {forYouItems.tours?.map((tour) => (
              <Card key={tour.id} item={tour} onClick={() => handleCardClick(tour.id, 'tour')} />
            ))}
          </div>
        </div>
      )}
      <div className="section featured">
        <h1 className="section-title"><FaGift className="section-icon" /> Featured Offers</h1>
        <div className="scrollable-row">
          {featuredItems.activities?.map((activity) => (
            <Card key={activity.id} item={activity} onClick={() => handleCardClick(activity.id, 'activity')} />
          ))}
          {featuredItems.packages?.map((pkg) => (
            <Card key={pkg.id} item={pkg} onClick={() => handleCardClick(pkg.id, 'package')} />
          ))}
          {featuredItems.tours?.map((tour) => (
            <Card key={tour.id} item={tour} onClick={() => handleCardClick(tour.id, 'tour')} />
          ))}
        </div>
      </div>
      <div className="section">
        <h1 className="section-title">Latest</h1>
        <div className="scrollable-row">
          {latestItems.activities?.map((activity) => (
            <Card key={activity.id} item={activity} onClick={() => handleCardClick(activity.id, 'activity')} />
          ))}
          {latestItems.packages?.map((pkg) => (
            <Card key={pkg.id} item={pkg} onClick={() => handleCardClick(pkg.id, 'package')} />
          ))}
          {latestItems.tours?.map((tour) => (
            <Card key={tour.id} item={tour} onClick={() => handleCardClick(tour.id, 'tour')} />
          ))}
        </div>
      </div>
      <div className='cat-offers'>
      <div className="section">
        <h1 className="section-title"><FaHiking className="section-icon" /> Activities
          <a href="/all-activities/" className="see-all-link">See All</a>
        </h1>
        <div className="scrollable-row">
          {activities?.map((activity) => (
            <Card key={activity.id} item={activity} onClick={() => handleCardClick(activity.id, 'activity')} />
          ))}
        </div>
      </div>
      <div className="section">
        <h1 className="section-title"><FaMapSigns className="section-icon" /> Tours
          <a href="/all-tours/" className="see-all-link">See All</a>
        </h1>
        <div className="scrollable-row">
          {tours?.map((tour) => (
            <Card key={tour.id} item={tour} onClick={() => handleCardClick(tour.id, 'tour')} />
          ))}
        </div>
      </div>
      <div className="section">
        <h1 className="section-title"><FaBoxOpen className="section-icon" /> Packages
          <a href="/all-packages/" className="see-all-link">See All</a>
        </h1>
        <div className="scrollable-row">
          {packages?.map((pkg) => (
            <Card key={pkg.id} item={pkg} onClick={() => handleCardClick(pkg.id, 'package')} />
          ))}
        </div>
      </div>
      </div>
    </div>
  );
};

export default MainPage;
