import React, { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { format, eachDayOfInterval } from 'date-fns';

const CustomDatePicker = ({ from, to, daysOff , onDateChange}) => {
  const [selectedDate, setSelectedDate] = useState(null);
  const [availableDates, setAvailableDates] = useState([]);
  
    // change the date and send it back to be used in periods
    const handleDateChange = (newValue)=>{
        setSelectedDate(newValue);
        const formattedDate = format(newValue, 'yyyy-MM-dd');
        onDateChange(formattedDate);
    }
  useEffect(() => {
    const startDate = new Date(from);
    const endDate = new Date(to);
    const dayOffList = daysOff.split(',').map(day => day.trim());

    const allDates = eachDayOfInterval({
      start: startDate,
      end: endDate
    });

    const filteredDates = allDates.filter(date => {
      const dayName = format(date, 'EEEE'); // Get day name (e.g., 'Saturday')
      return !dayOffList.includes(dayName);
    });

    setAvailableDates(filteredDates);
  }, [from, to, daysOff]);

  const isDateDisabled = (date) => {
    return !availableDates.some(availableDate =>
      format(availableDate, 'yyyy-MM-dd') === format(date, 'yyyy-MM-dd')
    );
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <DatePicker
        label="Select Date"
        value={selectedDate}
        onChange={handleDateChange}
        renderInput={(params) => <TextField {...params} />}
        shouldDisableDate={isDateDisabled}
      />
    </LocalizationProvider>
  );
};

export default CustomDatePicker;
