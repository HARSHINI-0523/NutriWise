// src/services/api.js
import axios from "axios";

// ✅ Define base URLs for different parts of your API
const FRIENDSHIP_API_URL = "http://localhost:5000/api/friendships";
const USER_API_URL = "http://localhost:5000/api/users";
const APPOINTMENT_API_URL = "http://localhost:5000/api/appointments";
// --- Existing Functions ---

export const fetchFriends = (userId) => {
  return axios.get(`${FRIENDSHIP_API_URL}/friends/${userId}`);
};

export const fetchReceivedRequests = (userId) => {
  return axios.get(`${FRIENDSHIP_API_URL}/requests/received/${userId}`);
};

export const respondToRequest = (friendshipId, action) => {
  return axios.post(`${FRIENDSHIP_API_URL}/requests/handle/${friendshipId}`, { action });
};

export const fetchSuggestions = (userId) => {
  return axios.get(`${FRIENDSHIP_API_URL}/suggestions/${userId}`);
};


/**
 * Searches for users based on a query string.
 */
export const searchUsers = (userId, query) => {
  // If the search query is empty, return an empty array without hitting the API
  if (!query) return Promise.resolve({ data: [] });
  
  return axios.get(`${USER_API_URL}/search/${userId}?query=${query}`);
};

/**
 * Sends a friend request from one user to another.
 */
export const sendFriendRequest = (requesterId, recipientId) => {
  return axios.post(`${FRIENDSHIP_API_URL}/request/send`, { requesterId, recipientId });
};


/**
 * Gets all appointments for a user.
 */
export const getAppointments = (userId) => {
  return axios.get(`${APPOINTMENT_API_URL}/${userId}`);
};

/**
 * Creates a new appointment.
 * @param {object} appointmentData - { title, start, end, user, notes }
 */
export const createAppointment = (appointmentData) => {
  return axios.post(APPOINTMENT_API_URL, appointmentData);
};

/**
 * Deletes an appointment by its ID.
 */
export const deleteAppointment = (appointmentId) => {
  return axios.delete(`${APPOINT-MENT_API_URL}/${appointmentId}`);
};