import React, { useState } from "react";
import "./SearchBar.css"; // Import the CSS file
import { FaSearch } from "react-icons/fa";
import api from '../services/api.js';
import Card from './Card';
import { useNavigate } from "react-router-dom";

const SearchBar = () => {
    const [searchResults, setSearchResults] = useState(null);
    const [query, setQuery] = useState('');
    const navigate = useNavigate();

    const handleSearch = async () => {
        try {
            const response = await api.get(`/api/search?query=${encodeURIComponent(query)}`);
            if (response.status == 200) {
                const data = await response.data;
                console.log("hi")
                console.log(data)
                setSearchResults(data);
            } else {
                console.error('Search request failed.');
            }
        } catch (error) {
                console.error('Error during fetch:', error);
        }
    };

  const handleCardClick = (id, type) => {
    navigate(`/${type}-details/${id}`);
  };

    return (
        <div>
            <div className="search-bar-container">
                <img src="/lebadvisor_logo.png" alt="Logo" className="logo" />
                <div className="search-bar">
                    <input
                        type="text"
                        placeholder="Search for activities, locations, tours and ideas"
                        className="search-input"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                    />
                    <button className="search-button" onClick={handleSearch}>
                        <FaSearch />
                    </button>
                </div>
            </div>
                        <br/><br/><br/><br/>
            <div >
                {searchResults ? (
                    <div className="search-results-container">
                {searchResults.activities ? searchResults.activities.map(activity => (
                  <Card key={activity.id} item={activity} onClick={() => handleCardClick(activity.id, 'activity')} />
                )): "no activities"}
                {searchResults.packages ? searchResults.packages.map(pkg => (
                  <Card key={pkg.id} item={pkg} onClick={() => handleCardClick(pkg.id, 'package')} />
                )): "no packages"}
                {searchResults.tours ? searchResults.tours.map(tour => (
                  <Card key={tour.id} item={tour} onClick={() => handleCardClick(tour.id, 'tour')} />
                )): "no tours"}
                    </div>
                ): 
                <br />}
            </div>
        </div>
    );
};

export default SearchBar;
