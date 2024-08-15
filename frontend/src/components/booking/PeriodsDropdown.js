import React, { useEffect, useState } from 'react';
import axios from 'axios';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import { MainUrl } from '../../services/api';

const PeriodsDropdown = ({ selectedDate, offerId, setSelectedPeriod, selectedPeriod }) => {
  const [periods, setPeriods] = useState([]);

  useEffect(() => {
    if (selectedDate && offerId) {
      fetchPeriods(selectedDate, offerId);
    }
  }, [selectedDate, offerId]);

  const fetchPeriods = async (date, offerId) => {
    try {
      const response = await axios.get(`${MainUrl}/api/offer/${offerId}/periods/${date}/`);
      setPeriods(response.data);
    } catch (error) {
      console.error('Error fetching periods:', error);
    }
  };

  const handlePeriodChange = (event) => {
    const periodId = event.target.value;
    const selected = periods.find(period => period.id === parseInt(periodId));
    setSelectedPeriod(selected);
  };

  return (
    <>
      <br />
      <br />
      <TextField
        select
        label="Select Period"
        value={selectedPeriod?.id || ''}
        onChange={handlePeriodChange}
        fullWidth
      >
        {periods.map((period) => (
          <MenuItem key={period.id} value={period.id}>
            from {period.time_from} till {period.time_to} - ${period.activity_offer.price} ({period.stock} available)
          </MenuItem>
        ))}
      </TextField>
    </>
  );
};

export default PeriodsDropdown;

