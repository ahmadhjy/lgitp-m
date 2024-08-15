import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import "./CardGrid.css";
import Card from '../Card.js';
import { Checkbox, FormControlLabel, FormGroup, Button, Select, MenuItem, InputLabel, FormControl } from '@mui/material';

const AllTours = () => {
  const [tours, setTours] = useState([]);
  const [categories, setCategories] = useState([]);
  const [locations, setLocations] = useState([]);
  const [selectedCategories, setSelectedCategories] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(0);
  const [showAllCategories, setShowAllCategories] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const toursResponse = await api.get('/api/all-tours/');
        setTours(toursResponse.data);
      } catch (error) {
        console.error('Failed to fetch data', error);
      }
    };

    const fetchCategories = async () => {
      try {
        const categoriesResponse = await api.get('/api/categories/');
        setCategories(categoriesResponse.data);
        setSelectedCategories(categoriesResponse.data.map(category => category.id)); // Select all categories by default
      } catch (error) {
        console.error('Failed to fetch categories', error);
      }
    };

    const fetchLocations = async () => {
      try {
        const locationsResponse = await api.get('/api/locations/');
        setLocations(locationsResponse.data);
        setSelectedLocation(0); // Default to all locations
      } catch (error) {
        console.error('Failed to fetch locations', error);
      }
    };

    fetchData();
    fetchCategories();
    fetchLocations();
  }, []);

  const handleCardClick = (id) => {
    navigate(`/tour-details/${id}`);
  };

  const handleCategoryChange = (event) => {
    const selectedCategoryId = parseInt(event.target.value);
    if (selectedCategories.includes(selectedCategoryId)) {
      setSelectedCategories(selectedCategories.filter(id => id !== selectedCategoryId));
    } else {
      setSelectedCategories([...selectedCategories, selectedCategoryId]);
    }
  };

  const handleLocationChange = (event) => {
    const selectedLocationId = parseInt(event.target.value);
    setSelectedLocation(selectedLocationId);
  };

  const filteredTours = tours.filter(item => {
    // Filter by selected categories
    if (selectedCategories.length > 0 && !selectedCategories.some(id => item.categories.includes(id))) {
      return false;
    }

    // Filter by selected location
    if (selectedLocation !== 0 && item.location.id !== selectedLocation) {
      return false;
    }

    return true;
  });

  return (
    <div className="container">
      <div className="filters">
        <h3>Filters</h3>
        <div className="filter-group">
          <InputLabel>Categories</InputLabel>
          <FormGroup>
            {categories.slice(0, showAllCategories ? categories.length : 5).map(category => (
              <FormControlLabel
                key={category.id}
                control={
                  <Checkbox
                    checked={selectedCategories.includes(category.id)}
                    onChange={handleCategoryChange}
                    value={category.id}
                  />
                }
                label={category.name}
              />
            ))}
          </FormGroup>
          {categories.length > 5 && (
            <Button onClick={() => setShowAllCategories(!showAllCategories)}>
              {showAllCategories ? 'Show Less' : 'Show More'}
            </Button>
          )}
        </div>
        <div className="filter-group">
          <FormControl fullWidth>
            <Select
              value={selectedLocation}
              onChange={handleLocationChange}
            >
              <MenuItem value={0}>All Locations</MenuItem>
              {locations.map(location => (
                <MenuItem key={location.id} value={location.id}>{location.name}</MenuItem>
              ))}
            </Select>
          </FormControl>
        </div>
      </div>
      <div className="scrollable-row">
        {filteredTours.map(item => (
          <Card key={item.id} item={item} onClick={() => handleCardClick(item.id)} />
        ))}
      </div>
    </div>
  );
};

export default AllTours;
