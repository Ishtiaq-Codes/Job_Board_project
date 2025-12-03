import React from 'react';
import { useJobs } from '../context/JobContext';

function JobCard({ job }) {
  const { deleteJob, showJobForm } = useJobs();

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this job?')) {
      const result = await deleteJob(job.id);
      if (!result.success) {
        alert(`Failed to delete job: ${result.error}`);
      }
    }
  };

  const handleEdit = () => {
    showJobForm(job);
  };

  return (
    <div className="card p-6">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            {job.title}
          </h3>
          <div className="flex items-center text-gray-600 mb-2 space-x-4">
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
              </svg>
              {job.company}
            </span>
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
              </svg>
              {job.location}
            </span>
          </div>
          <div className="flex items-center text-sm text-gray-500 mb-3">
            <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clipRule="evenodd" />
            </svg>
            Posted: {job.posting_date}
          </div>
        </div>
        <div className="flex space-x-2 ml-4">
          <button
            onClick={handleEdit}
            className="btn-secondary text-sm"
          >
            Edit
          </button>
          <button
            onClick={handleDelete}
            className="btn-danger text-sm"
          >
            Delete
          </button>
        </div>
      </div>
      
      <div className="flex flex-wrap gap-2 mb-4">
        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
          {job.job_type}
        </span>
        {job.tags && job.tags.map((tag, index) => (
          <span
            key={index}
            className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800"
          >
            {tag}
          </span>
        ))}
      </div>
    </div>
  );
}

export default JobCard;

