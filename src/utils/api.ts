interface ApiConfig {
  method?: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  headers?: Record<string, string>;
  body?: any;
}

export const apiCall = async (url: string, config: ApiConfig = {}) => {
  const defaultHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  // Get the API key from your auth context or local storage
  const apiKey = localStorage.getItem('api_key');
  if (apiKey) {
    defaultHeaders['x-api-key'] = apiKey;
  }

  // Get the auth token from your auth context or local storage
  const token = localStorage.getItem('access_token');
  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`;
  }

  const headers = {
    ...defaultHeaders,
    ...config.headers,
  };

  try {
    const response = await fetch(url, {
      method: config.method || 'GET',
      headers,
      credentials: 'include', // Important for CORS with credentials
      body: config.body ? JSON.stringify(config.body) : undefined,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'API request failed');
    }

    return await response.json();
  } catch (error) {
    console.error('API call error:', error);
    throw error;
  }
}; 