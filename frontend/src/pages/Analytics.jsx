import React, { useEffect, useState } from "react";
import Navbar from "../components/common/Navbar";
import axios from "axios";

export default function Analytics() {

  const [stats, setStats] = useState(null);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {

    try {

      const token = localStorage.getItem("access_token");

      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/api/analytics/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setStats(response.data);

    } catch (error) {

      console.error(
        "Analytics fetch failed:",
        error.response?.data || error
      );

    } finally {

      setLoading(false);

    }
  };

  if (loading) {

    return (
      <>
        <Navbar />

        <h2
          style={{
            padding: "30px",
          }}
        >
          Loading analytics...
        </h2>
      </>
    );
  }

  if (!stats) {

    return (
      <>
        <Navbar />

        <h2
          style={{
            padding: "30px",
          }}
        >
          Failed to load analytics
        </h2>
      </>
    );
  }

  return (

    <>
      <Navbar />

      <div
        style={{
          padding: "30px",
          background: "#eef7f0",
          minHeight: "100vh",
        }}
      >

        <h1
          style={{
            color: "#1b4332",
            marginBottom: "30px",
            fontSize: "40px",
            fontWeight: "bold",
          }}
        >
          Analytics Dashboard
        </h1>

        {/* TOP CARDS */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(250px,1fr))",
            gap: "20px",
          }}
        >

          <div style={cardStyle}>

            <div style={iconStyle}>
              📊
            </div>

            <h2>Total Predictions</h2>

            <p style={numberStyle}>
              {stats.total_predictions}
            </p>

          </div>

          <div style={cardStyle}>

            <div style={iconStyle}>
              ✅
            </div>

            <h2>Healthy Leaves</h2>

            <p style={numberStyle}>
              {stats.healthy_predictions}
            </p>

          </div>

          <div style={cardStyle}>

            <div style={iconStyle}>
              🦠
            </div>

            <h2>Disease Detections</h2>

            <p style={numberStyle}>
              {stats.disease_predictions}
            </p>

          </div>

        </div>

        {/* BREAKDOWN */}
        <div
          style={{
            marginTop: "40px",
            background: "white",
            padding: "30px",
            borderRadius: "18px",
            boxShadow:
              "0 4px 14px rgba(0,0,0,0.08)",
          }}
        >

          <h2
            style={{
              marginBottom: "25px",
              fontSize: "28px",
              color: "#081c15",
            }}
          >
            Disease Breakdown
          </h2>

          {stats.disease_breakdown?.map(
            (item, index) => (

              <div
                key={index}
                style={{
                  marginBottom: "24px",
                }}
              >

                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    marginBottom: "8px",
                    fontSize: "18px",
                  }}
                >

                  <strong>
                    {item.name}
                  </strong>

                  <span>
                    {item.count}
                  </span>

                </div>

                <div
                  style={{
                    width: "100%",
                    height: "16px",
                    background: "#d8f3dc",
                    borderRadius: "20px",
                    overflow: "hidden",
                  }}
                >

                  <div
                    style={{
                      width: `${item.percentage}%`,
                      height: "100%",
                      background: "#2d6a4f",
                      transition: "1s",
                    }}
                  />

                </div>

              </div>

            )
          )}

        </div>

      </div>
    </>
  );
}

const cardStyle = {

  background: "white",

  borderRadius: "18px",

  padding: "28px",

  boxShadow:
    "0 4px 14px rgba(0,0,0,0.08)",

  display: "flex",

  flexDirection: "column",

  gap: "10px",
};

const iconStyle = {

  fontSize: "34px",

  width: "60px",

  height: "60px",

  borderRadius: "14px",

  background: "#eef7f0",

  display: "flex",

  alignItems: "center",

  justifyContent: "center",
};

const numberStyle = {

  fontSize: "48px",

  fontWeight: "bold",

  color: "#2d6a4f",

  marginTop: "10px",
};