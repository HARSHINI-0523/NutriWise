import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./ReportViewer.css";

const ReportViewer = () => {
  const navigate = useNavigate();
  const { state: report } = useLocation();
  console.log("ANALYSIS RAW => ", report.analysis);
  console.log("VALUES RAW => ", report.values);

  
  if (!report) {
    return (
      <div className="viewer-container">
        <p>Report data not found.</p>
        <button className="back-btn" onClick={() => navigate(-1)}>
          Go Back
        </button>
      </div>
    );
  }

  return (
    <div className="viewer-container">
      {/* Back Button */}
      <div className="viewer-header">
        <button className="back-btn" onClick={() => navigate(-1)}>
          ← Back
        </button>
      </div>

      {/* File Link */}
      <div className="report-link-card">
        <p>📄 Original Report File</p>
        <a
          href={report.fileURL}
          target="_blank"
          rel="noopener noreferrer"
          className="report-link"
        >
          Open Report
        </a>
      </div>

      {/* Extracted Values */}
      <div className="section-card">
        <h3>Extracted Lab Values</h3>

        {report.values && Object.keys(report.values).length > 0 ? (
          <table className="values-table">
            <thead>
              <tr>
                <th>Test</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(report.values).map(([key, value]) => (
                <tr key={key}>
                  <td>{key}</td>
                  <td>{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="muted-text">No values extracted.</p>
        )}
      </div>

      {/* AI Summary */}
      <div className="section-card ai-card">
        <h3>AI Health Summary</h3>

        <div className="ai-text">
          {String(report.analysis)
            .replace(/\\n/g, "\n") // convert escaped → real newlines
            .replace(/\\"/g, '"')}{" "}
          // optional: fix escaped quotes
        </div> 
        

        <div className="ai-warning">
          ⚠️ AI-generated insights only. Consult a doctor for diagnosis.
        </div>
      </div>
    </div>
  );
};

export default ReportViewer;
