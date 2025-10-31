import React from 'react';
import { useJobs } from '../context/JobContext';
import SearchBox from './SearchBox';
import DropdownFilter from './DropdownFilter';
import SortDropdown from './SortDropdown';

function FilterBar() {
  const { filters, resetFilters } = useJobs();

  const jobTypeOptions = ['Full-time', 'Part-time', 'Contract', 'Internship'];
  const locationOptions = ['Remote', 'New York', 'Chicago', 'London', 'Boston', 'Austin'];
  const tagOptions = ['Life', 'Health', 'Pricing', 'Python', 'SQL', 'R', 'Modeling'];

  const hasActiveFilters = Object.values(filters).some(value => value && value !== 'All');

  return (
    <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200 mb-6">
      <div className="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-4 mb-4">
        <div className="flex-1">
          <SearchBox />
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 flex-1">
          <DropdownFilter
            type="jobType"
            options={jobTypeOptions}
            label="Job Types"
          />
          <DropdownFilter
            type="location"
            options={locationOptions}
            label="Locations"
          />
          <DropdownFilter
            type="tag"
            options={tagOptions}
            label="Tags"
          />
          <SortDropdown />
        </div>
      </div>

      {/* Active Filters Display */}
      {hasActiveFilters && (
        <div className="flex items-center justify-between pt-4 border-t border-gray-200">
          <div className="flex items-center space-x-2">
            <span className="text-sm text-gray-600">Active filters:</span>
            {filters.search && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-800">
                Search: "{filters.search}"
              </span>
            )}
            {filters.jobType && filters.jobType !== 'All' && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                {filters.jobType}
              </span>
            )}
            {filters.location && filters.location !== 'All' && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-purple-100 text-purple-800">
                {filters.location}
              </span>
            )}
            {filters.tag && filters.tag !== 'All' && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-orange-100 text-orange-800">
                {filters.tag}
              </span>
            )}
          </div>
          
          <button
            onClick={resetFilters}
            className="text-sm text-blue-600 hover:text-blue-800 font-medium"
          >
            Reset All Filters
          </button>
        </div>
      )}
    </div>
  );
}

export default FilterBar;