import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export const predictionService = {
  predict: async (formData) => {
    try {
      const response = await axios.post(
        `${API_URL}/predict`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      return response.data;
    } catch (error) {
      console.error("Prediction error:", error);
      throw error;
    }
  },
};