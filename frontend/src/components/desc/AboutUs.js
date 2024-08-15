import React from 'react';
import './AboutUs.css';

const AboutUs = () => {
  return (
    <div className="about-us">
      <h2>About Us</h2>
      <p>
        Welcome to our application, the ultimate connection between suppliers and people looking for things to do in Lebanon. We offer a variety of tours, activities, and packages that cater to all interests and preferences. Whether you're seeking adventure, relaxation, or cultural experiences, we've got you covered.
      </p>
      <p>
        Our platform includes a comprehensive booking system that benefits both suppliers and users, ensuring a smooth and efficient process for everyone involved.
      </p>
      <div className="contact-info">
        <h3>Contact Us</h3>
        <p>Email: info@example.com</p>
        <p>Phone: +961-12345678</p>
      </div>
    </div>
  );
};

export default AboutUs;
