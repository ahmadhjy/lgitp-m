import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import MainPage from "./components/MainPage.js";
import ActivityDetails from "./components/ActivityDetails.js";
import PackageDetails from "./components/PackageDetails.js";
import TourDetails from "./components/TourDetails.js";
import Navbar from "./components/Navbar.js";
import Footer from "./components/Footer.js";
import Bookings from "./components/CustomerBookingPage.js";
import SupplierBookings from "./components/SupplierBookingPage.js";
import PrivacyPolicy from "./components/desc/PrivacyPolicy.js";
import TermsOfService from "./components/desc/TermsOfService.js";
import ContactUs from "./components/desc/ContactUs.js";
import AboutUs from "./components/desc/AboutUs.js";
import AllActivities from "./components/displayall/AllActivities.js";
import AllTours from "./components/displayall/AllTours.js";
import AllPackages from "./components/displayall/AllPackages.js";
import SearchBar from "./components/SearchBar.js";
import Profile from "./components/Profile.js";
import Favorites from "./components/Favorites.js";
import NotificationsPage from "./components/NotificationsPage.js";
import PostList from './components/PostList';
import PostDetail from './components/PostDetail';

function App() { 
    return (
        <Router>
            {/* navbar is outside routes, a god above all */}
            <Navbar />
            <Routes>
                <Route path="/" element={localStorage.getItem('s') ?<SupplierBookings /> : <MainPage /> } />
                <Route path="/favorites/" element={<Favorites />} />
                <Route path="/search/" element={<SearchBar />} />
                <Route path="/profile/" element={<Profile />} />
                <Route
                    path="/activity-details/:id"
                    element={<ActivityDetails />}
                />
                <Route path="/tour-details/:id" element={<TourDetails />} />
                <Route
                    path="/package-details/:id"
                    element={<PackageDetails />}
                />
                <Route path="/bookings" element={localStorage.getItem('s') ?<SupplierBookings /> : <Bookings />} />
                <Route
                    path="/supplier-bookings/"
                    element={<SupplierBookings />}
                />
                <Route path="/privacy-policy/" element={<PrivacyPolicy />} />
                <Route path="/terms-of-service/" element={<TermsOfService />} />
                <Route path="/contact-us/" element={<ContactUs />} />
                <Route path="/about-us/" element={<AboutUs />} />
                <Route path="/all-activities/" element={<AllActivities />} />
                <Route path="/all-packages/" element={<AllPackages />} />
                <Route path="/all-tours/" element={<AllTours />} />
                <Route path="/notifications/" element={<NotificationsPage />} />
                <Route path="/blog" element={<PostList />} />  {/* Route for Blog List */}
                <Route path="/blog/post/:id" element={<PostDetail />} />  {/* Route for Blog Post Detail */}
            </Routes>

            {/* footer is outside routes, just an outsider that is everywhere */}
            <Footer />
        </Router>
    );
}
export default App;
