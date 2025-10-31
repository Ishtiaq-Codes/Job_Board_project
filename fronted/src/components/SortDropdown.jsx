import React from 'react';
import { useJobs } from '../context/JobContext';

function SortDropdown() {
  const { sort, setSort } = useJobs();

  const sortOptions = [
    { value: 'posting_date_desc', label: 'Date Posted: Newest First' },
    { value: 'posting_date_asc', label: 'Date Posted: Oldest First' },
    { value: 'title_asc', label: 'Title: A to Z' },
    { value: 'title_desc', label: 'Title: Z to A' },
    { value: 'company_asc', label: 'Company: A to Z' },
  ];

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Sort By
      </label>
      <select
        value={sort}
        onChange={(e) => setSort(e.target.value)}
        className="input-field"
      >
        {sortOptions.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}

export default SortDropdown;