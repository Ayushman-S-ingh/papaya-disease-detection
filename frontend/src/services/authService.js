import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export const authService = {
  login: async (email, password) => {
    try {
      const response = await axios.post(`${API_URL}/login`, {
        email,
        password,
      });

      return response.data;
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  },

  register: async (userData) => {
    try {
      const response = await axios.post(
        `${API_URL}/register`,
        userData
      );

      return response.data;
    } catch (error) {
      console.error("Register error:", error);
      throw error;
    }
  },
};