import React from 'react';
import { FaMountain, FaHiking, FaHotel, FaCalendarAlt, FaCompass, FaHeart, FaLeaf, FaHandsHelping } from 'react-icons/fa';
import './AboutUs.css';

const AboutUs = () => {
  return (
    <div className="about-us-container">
      <div className="about-us-hero">
        <h1>About LebAdvisor</h1>
        <p>Discover the best of Lebanon with our full-day tours, packages, and outdoor activities.</p>
      </div>

      <div className="about-us-content">
        <section className="mission">
          <h2>Our Mission</h2>
          <p>
            At LebAdvisor, our mission is to offer unforgettable experiences in Lebanon through carefully curated full-day tours, diverse packages, and exciting outdoor activities. We aim to connect travelers with the rich cultural heritage, natural beauty, and vibrant life of Lebanon. Whether you are seeking adventure, relaxation, or a deep cultural dive, LebAdvisor is your gateway to Lebanon's hidden gems.
          </p>
        </section>

        <section className="services">
          <h2>What We Offer</h2>
          <div className="services-list">
            <div className="service-item">
              <FaMountain className="service-icon" />
              <h3>Full-Day Tours</h3>
              <p>Explore Lebanon's iconic destinations and hidden gems with our expertly guided full-day tours, designed to offer a comprehensive experience of the country's beauty.</p>
            </div>
            <div className="service-item">
              <FaHiking className="service-icon" />
              <h3>Outdoor Activities</h3>
              <p>From hiking and biking to water sports and adventure trails, we offer a wide range of outdoor activities that cater to thrill-seekers and nature lovers alike.</p>
            </div>
            <div className="service-item">
              <FaHotel className="service-icon" />
              <h3>Packages</h3>
              <p>Enjoy carefully crafted packages that bundle together accommodation, activities, and more, ensuring a seamless and hassle-free travel experience in Lebanon.</p>
            </div>
            <div className="service-item">
              <FaCalendarAlt className="service-icon" />
              <h3>Advanced Booking System</h3>
              <p>Our state-of-the-art booking system simplifies the process of planning, booking, and managing your trips, offering flexibility and convenience at your fingertips.</p>
            </div>
          </div>
        </section>

        <section className="values">
          <h2>Our Values</h2>
          <ul>
            <li><FaCompass className="value-icon" /><strong>Authenticity:</strong> We provide experiences that reflect the true essence of Lebanon, connecting travelers with genuine local culture.</li>
            <li><FaHeart className="value-icon" /><strong>Quality:</strong> We partner with trusted suppliers to ensure the highest standards of service and satisfaction for our customers.</li>
            <li><FaLeaf className="value-icon" /><strong>Sustainability:</strong> We are committed to promoting sustainable tourism practices that preserve Lebanon's natural and cultural heritage for future generations.</li>
            <li><FaHandsHelping className="value-icon" /><strong>Community:</strong> We believe in supporting local communities by promoting small businesses and local guides, fostering a deeper connection between travelers and the people of Lebanon.</li>
          </ul>
        </section>

        <section className="contact-info">
          <h2>Contact Us</h2>
          <p>We are here to assist you in planning your perfect Lebanese adventure. Feel free to reach out with any inquiries.</p>
          <p><strong>Email:</strong> <a href="mailto:info@lebadvisor.com">info@lebadvisor.com</a></p>
          <p><strong>Phone:</strong> +961 71 941 100</p>
        </section>
      </div>
    </div>
  );
};

export default AboutUs;
