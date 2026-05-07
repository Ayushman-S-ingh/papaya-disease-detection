export default function ConfidenceBar({ confidence = 0 }) {
  return (
    <div style={{ marginTop: "20px" }}>
      <p>Confidence: {confidence}%</p>

      <div
        style={{
          width: "100%",
          height: "20px",
          background: "#ddd",
          borderRadius: "10px",
        }}
      >
        <div
          style={{
            width: `${confidence}%`,
            height: "100%",
            background: "green",
            borderRadius: "10px",
          }}
        ></div>
      </div>
    </div>
  );
}