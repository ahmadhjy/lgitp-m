import React, { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { format } from 'date-fns';

const PackageDatePicker = ({ availablePackageDays, onDateChange }) => {
  const [selectedDate, setSelectedDate] = useState(null);

  const handleDateChange = (newValue) => {
    setSelectedDate(newValue);
    const formattedDate = format(newValue, 'yyyy-MM-dd');
    onDateChange(formattedDate);
  };

  const isDateDisabled = (date) => {
    return !availablePackageDays.includes(format(date, 'yyyy-MM-dd'));
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <DatePicker
        label="Select Start Date"
        value={selectedDate}
        onChange={handleDateChange}
        renderInput={(params) => <TextField {...params} />}
        shouldDisableDate={isDateDisabled}
      />
    </LocalizationProvider>
  );
};

export default PackageDatePicker;
