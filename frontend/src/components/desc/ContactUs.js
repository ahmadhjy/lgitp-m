import React from 'react';
import PhoneIcon from '@mui/icons-material/Phone';
import EmailIcon from '@mui/icons-material/Email';
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
                    <PhoneIcon className="contact-method-icon" />
                    <h2 className="contact-method-title">Phone</h2>
                    <p className="contact-method-detail">+961 71 941 100</p>
                </div>

                <div className="contact-method">
                    <EmailIcon className="contact-method-icon" />
                    <h2 className="contact-method-title">Email</h2>
                    <p className="contact-method-detail"><a href="mailto:info@lebadvisor.com">info@lebadvisor.com</a></p>
                </div>
            </div>

            <iframe
                id="JotFormIFrame-242277018965464"
                title="Contact LebAdvisor"
                onLoad={() => window.parent.scrollTo(0, 0)}
                allowTransparency="true"
                allow="geolocation; microphone; camera; fullscreen"
                src="https://form.jotform.com/242277018965464"
                frameBorder="0"
                scrolling="no"
            ></iframe>
        </div>
    );
};

export default ContactUs;
