import axios from "axios";
import { getSession, useSession } from "next-auth/react";

// Create an Axios instance with a base URL
const useAxios = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

// Request interceptor
useAxios.interceptors.request.use(
  async (config) => {
    // Get the session using the request's referer (if available)
    const session = await getSession({ req: config.headers.referer });

    // If a valid session with an access token exists, add it to the request headers
    if (session?.access_token) {
      config.headers.Authorization = `Bearer ${session.access_token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
useAxios.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // If the response status is 401 (Unauthorized) and it's not a retried request
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      // Get the session using useSession
      const session = await useSession();

      // Get the refresh token
      const refresh_token = session.data?.refresh_token;

      // Send a request to refresh the access token
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/refresh`,
        null,
        {
          headers: {
            Authorization: `Bearer ${refresh_token}`,
          },
        }
      );

      if (response.status === 200) {
        // Update the session with the new access token
        session.update(response.data.access_token);

        // Update the request headers with the new access token
        originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;

        // Retry the original request
        return axios(originalRequest);
      }
    }

    return Promise.reject(error);
  }
);

export default useAxios;
