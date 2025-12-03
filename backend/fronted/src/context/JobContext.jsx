import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { jobAPI } from '../utils/API';

const JobContext = createContext();

const initialState = {
  jobs: [],
  loading: false,
  error: null,
  filters: {
    search: '',
    jobType: 'All',
    location: 'All',
    tag: 'All'
  },
  sort: 'posting_date_desc',
  showForm: false,
  editingJob: null
};

function jobReducer(state, action) {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    
    case 'SET_JOBS':
      return { ...state, jobs: action.payload, loading: false };
    
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    
    case 'SET_FILTERS':
      return { ...state, filters: { ...state.filters, ...action.payload } };
    
    case 'SET_SORT':
      return { ...state, sort: action.payload };
    
    case 'SHOW_FORM':
      return { ...state, showForm: true, editingJob: action.payload || null };
    
    case 'HIDE_FORM':
      return { ...state, showForm: false, editingJob: null };
    
    case 'ADD_JOB':
      return { ...state, jobs: [action.payload, ...state.jobs] };
    
    case 'UPDATE_JOB':
      return {
        ...state,
        jobs: state.jobs.map(job => 
          job.id === action.payload.id ? action.payload : job
        )
      };
    
    case 'DELETE_JOB':
      return {
        ...state,
        jobs: state.jobs.filter(job => job.id !== action.payload)
      };
    
    case 'RESET_FILTERS':
      return {
        ...state,
        filters: initialState.filters,
        sort: initialState.sort
      };
    
    default:
      return state;
  }
}

export function JobProvider({ children }) {
  const [state, dispatch] = useReducer(jobReducer, initialState);

  // Fetch jobs with current filters
  const fetchJobs = async () => {
    dispatch({ type: 'SET_LOADING', payload: true });
    try {
      const jobs = await jobAPI.getJobs(state.filters, state.sort);
      dispatch({ type: 'SET_JOBS', payload: jobs });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
    }
  };

  const addJob = async (jobData) => {
    try {
      const newJob = await jobAPI.createJob(jobData);
      dispatch({ type: 'ADD_JOB', payload: newJob });
      dispatch({ type: 'HIDE_FORM' });
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const updateJob = async (jobId, jobData) => {
    try {
      const updatedJob = await jobAPI.updateJob(jobId, jobData);
      dispatch({ type: 'UPDATE_JOB', payload: updatedJob });
      dispatch({ type: 'HIDE_FORM' });
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const deleteJob = async (jobId) => {
    try {
      await jobAPI.deleteJob(jobId);
      dispatch({ type: 'DELETE_JOB', payload: jobId });
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  };

  const setFilters = (filters) => {
    dispatch({ type: 'SET_FILTERS', payload: filters });
  };

  const setSort = (sort) => {
    dispatch({ type: 'SET_SORT', payload: sort });
  };

  const showJobForm = (job = null) => {
    dispatch({ type: 'SHOW_FORM', payload: job });
  };

  const hideJobForm = () => {
    dispatch({ type: 'HIDE_FORM' });
  };

  const resetFilters = () => {
    dispatch({ type: 'RESET_FILTERS' });
  };

  // Fetch jobs when filters or sort change
  useEffect(() => {
    fetchJobs();
  }, [state.filters, state.sort]);

  const value = {
    ...state,
    fetchJobs,
    addJob,
    updateJob,
    deleteJob,
    setFilters,
    setSort,
    showJobForm,
    hideJobForm,
    resetFilters
  };

  return (
    <JobContext.Provider value={value}>
      {children}
    </JobContext.Provider>
  );
}

export function useJobs() {
  const context = useContext(JobContext);
  if (!context) {
    throw new Error('useJobs must be used within a JobProvider');
  }
  return context;
}