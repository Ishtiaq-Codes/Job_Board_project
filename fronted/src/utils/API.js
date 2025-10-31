const API_BASE = 'http://localhost:5000/api';

async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Network error' }));
    throw new Error(error.error || `HTTP error! status: ${response.status}`);
  }
  return response.json();
}

export const jobAPI = {
  async getJobs(filters = {}, sort = 'posting_date_desc') {
    const params = new URLSearchParams();
    
    // Add filters
    Object.entries(filters).forEach(([key, value]) => {
      if (value && value !== 'All') {
        params.append(key, value);
      }
    });
    
    // Add sort
    if (sort) {
      params.append('sort', sort);
    }
    
    const url = `${API_BASE}/jobs${params.toString() ? `?${params.toString()}` : ''}`;
    const response = await fetch(url);
    return handleResponse(response);
  },

  async getJob(id) {
    const response = await fetch(`${API_BASE}/jobs/${id}`);
    return handleResponse(response);
  },

  async createJob(jobData) {
    const response = await fetch(`${API_BASE}/jobs`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(jobData),
    });
    return handleResponse(response);
  },

  async updateJob(id, jobData) {
    const response = await fetch(`${API_BASE}/jobs/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(jobData),
    });
    return handleResponse(response);
  },

  async deleteJob(id) {
    const response = await fetch(`${API_BASE}/jobs/${id}`, {
      method: 'DELETE',
    });
    if (response.status === 204) {
      return {};
    }
    return handleResponse(response);
  },
};