import React from 'react';
import './ContactUs.css';

const ContactUs = () => {
    return (
        <div className="contact-container">
            <h1 className="contact-title">Contact Us</h1>
            <p className="contact-description">
                We would love to hear from you! You can reach us through the following methods:
            </p>

            <div className="contact-info">
                <div className="contact-method">
                    <h2 className="contact-method-title">Phone</h2>
                    <p className="contact-method-detail">+961 71 941 100</p>
                </div>

                <div className="contact-method">
                    <h2 className="contact-method-title">Email</h2>
                    <p className="contact-method-detail"><a href="mailto:info@lebadvisor.com">info@lebadvisor.com</a></p>
                </div>
            </div>
        </div>
    );
};

export default ContactUs;
