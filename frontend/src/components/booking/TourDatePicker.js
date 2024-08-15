import React, { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { format } from 'date-fns';

const TourDatePicker = ({ availableTourDays, onDateChange }) => {
  const [selectedDate, setSelectedDate] = useState(null);

  // Handle date change
  const handleDateChange = (newValue) => {
    setSelectedDate(newValue);
    const formattedDate = format(newValue, 'yyyy-MM-dd');
    onDateChange(formattedDate);
  };

  // Check if a date is disabled
  const isDateDisabled = (date) => {
    return !availableTourDays.includes(format(date, 'yyyy-MM-dd'));
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <DatePicker
        label="Select Tour Date"
        value={selectedDate}
        onChange={handleDateChange}
        renderInput={(params) => <TextField {...params} />}
        shouldDisableDate={isDateDisabled}
      />
    </LocalizationProvider>
  );
};

export default TourDatePicker;

