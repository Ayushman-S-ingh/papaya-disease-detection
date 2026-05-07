import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

export const predictionService = {

  // ── Predict Disease ─────────────────────────────────────
  predict: async (file, notes) => {
    try {
      const formData = new FormData();

      formData.append("image", file);
      formData.append("notes", notes || "");

      const response = await axios.post(
        `${API_URL}/api/predict`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        }
      );

      return response.data;

    } catch (error) {
      console.error("Prediction error:", error.response?.data);
      throw error;
    }
  },

  // ── Dashboard Summary ──────────────────────────────────
  getSummary: async () => {
    return {
      total_predictions: 12,
      avg_confidence: 94,
      disease_distribution: {
        "Healthy Leaf": 5,
        "Leaf Curl Disease": 3,
        "Powdery Mildew": 2,
      },
    };
  },

  // ── Prediction History ─────────────────────────────────
  getHistory: async () => {
    return {
      predictions: [
        {
          id: 1,
          disease_name: "Healthy Leaf",
          confidence: 98,
          severity: "none",
          created_at: new Date(),
        },
        {
          id: 2,
          disease_name: "Leaf Curl Disease",
          confidence: 91,
          severity: "medium",
          created_at: new Date(),
        },
      ],
    };
  },

  // ── Download PDF Report ────────────────────────────────
  getReport: async (predictionId) => {
    try {
      const response = await axios.get(
        `${API_URL}/api/report/${predictionId}`,
        {
          responseType: "blob",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        }
      );

      return response.data;

    } catch (error) {
      console.error("Report download error:", error);
      throw error;
    }
  },
};