import React, { useState } from "react";
import { useAuth } from "../../contexts/UserLoginContext.jsx";
import { useToast } from "../../contexts/ToastContext.jsx";
import "./UploadReport.css";
import api from "../../api/axios.js";

const reportTypes = [
  "Blood Test",
  "Urine Analysis",
  "Imaging Scan (X-Ray, MRI, CT)",
  "Genetic Report",
  "Other Medical Document",
];

const UploadReport = () => {
  const { currentUser } = useAuth();
  const { showToast } = useToast();

  const [file, setFile] = useState(null);
  const [reportType, setReportType] = useState(reportTypes[0]);
  const [isLoading, setIsLoading] = useState(false);

  const UPLOAD_API_ENDPOINT = "http://localhost:5000/api/reports/upload";

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.size > 5 * 1024 * 1024) {
        showToast("File size exceeds 5MB limit.", "error");
        setFile(null);
        return;
      }
      setFile(selectedFile);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      showToast("Please select a file to upload.", "error");
      return;
    }

    // // **CHECK 1:** Make sure the user is authenticated and has a token
    // if (!currentUser || !currentUser.token) {
    //   showToast("You must be logged in to upload a report.", "error");
    //   return;
    // }

    if (!currentUser) {
      showToast("You must be logged in", "error");
      return;
    }

    setIsLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("reportType", reportType);

    try {
      await api.post("/reports/upload", formData);
      showToast("File uploaded successfully!", "success");
      setFile(null);
      setReportType(reportTypes[0]);
    } catch (err) {
      showToast(err.response?.data?.message || "Upload failed", "error");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="upload-report-container">
      <h2 className="upload-report-header">Upload Medical Report</h2>

      <form onSubmit={handleUpload} className="upload-form">
        {/* 1. Report Type Selection */}
        <div className="form-group">
          <label htmlFor="reportType">Report Type</label>
          <select
            id="reportType"
            value={reportType}
            onChange={(e) => setReportType(e.target.value)}
            required
            disabled={isLoading}
          >
            {reportTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>

        {/* 2. File Input */}
        <div className="form-group">
          <label htmlFor="reportFile">Select File (Max 5MB)</label>
          <input
            type="file"
            id="reportFile"
            accept=".pdf,.jpg,.jpeg,.png"
            onChange={handleFileChange}
            required
            disabled={isLoading}
          />
          {file && (
            <p className="file-info">
              Selected: <strong>{file.name}</strong> (
              {Math.round(file.size / 1024)} KB)
            </p>
          )}
        </div>

        {/* 3. Submission Button */}
        <div>
          <button
            type="submit"
            className="report-upload-btn"
            disabled={isLoading || !file}
          >
            {isLoading ? "Uploading..." : "Upload Report"}
          </button>
          <button
            type="submit"
            className="report-upload-btn"
            disabled={isLoading || !file}
          >
            {isLoading ? "Generating..." : "Generate Analysis"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default UploadReport;
