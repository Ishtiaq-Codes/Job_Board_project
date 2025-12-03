import React from 'react';
import { JobProvider, useJobs } from './context/JobContext';
import JobList from './components/jobList';
import FilterBar from './components/FilterBar';
import JobForm from './components/JobForm';

function AppContent() {
  const { showForm, showJobForm, jobs, loading } = useJobs();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Actuary Jobs</h1>
              <p className="text-gray-600 mt-1">Find your next actuarial opportunity</p>
            </div>
            <button
              onClick={() => showJobForm()}
              className="btn-primary"
            >
              Post a Job
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Bar */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
          <div className="flex flex-wrap gap-6 text-center">
            <div>
              <div className="text-2xl font-bold text-gray-900">{jobs.length}</div>
              <div className="text-sm text-gray-600">Total Jobs</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">
                {jobs.filter(job => job.job_type === 'Full-time').length}
              </div>
              <div className="text-sm text-gray-600">Full-time</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">
                {jobs.filter(job => job.location.toLowerCase().includes('remote')).length}
              </div>
              <div className="text-sm text-gray-600">Remote</div>
            </div>
          </div>
        </div>

        {/* Filters */}
        <FilterBar />

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-gray-600">Loading jobs...</span>
          </div>
        )}

        {/* Job List */}
        <JobList />
      </main>

      {/* Job Form Modal */}
      {showForm && <JobForm />}
    </div>
  );
}

function App() {
  return (
    <JobProvider>
      <AppContent />
    </JobProvider>
  );
}

export default App;