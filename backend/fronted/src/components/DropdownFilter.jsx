import React from 'react';
import { useJobs } from '../context/JobContext';

function DropdownFilter({ type, options, label }) {
  const { filters, setFilters } = useJobs();

  const handleChange = (e) => {
    setFilters({ [type]: e.target.value });
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </label>
      <select
        value={filters[type] || 'All'}
        onChange={handleChange}
        className="input-field"
      >
        <option value="All">All {label}</option>
        {options.map(option => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    </div>
  );
}

export default DropdownFilter;