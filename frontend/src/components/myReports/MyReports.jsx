import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/UserLoginContext.jsx';
import { useToast } from '../../contexts/ToastContext.jsx';
import './MyReports.css';

const MyReports = () => {
  const { currentUser } = useAuth();
  const { showToast } = useToast();

  const [reports, setReports] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReports = async () => {
      // Check if user is logged in
      if (!currentUser || !currentUser.token) {
        setIsLoading(false);
        setError("You must be logged in to view your reports.");
        return;
      }

      try {
        const response = await fetch('http://localhost:5000/api/reports/me', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${currentUser.token}`,
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'Failed to fetch reports.');
        }

        const data = await response.json();
        setReports(data);

      } catch (err) {
        setError(err.message);
        showToast(err.message, "error");
        console.error("Failed to fetch reports:", err);

      } finally {
        setIsLoading(false);
      }
    };

    fetchReports();
  }, [currentUser, showToast]); // Re-run effect if currentUser or showToast changes

  if (isLoading) {
    return <div className="loading-container">Loading your reports...</div>;
  }

  if (error) {
    return <div className="error-container">Error: {error}</div>;
  }

  if (reports.length === 0) {
    return (
      <div className="no-reports-container">
        <h2>My Reports</h2>
        <p>You haven't uploaded any reports yet.</p>
      </div>
    );
  }

  return (
    <div className="reports-container">
      <h2>My Reports</h2>
      <div className="reports-list">
        {reports.map((report) => (
          <div key={report._id} className="report-card">
            <div className="report-header">
              <h3 className="report-title">{report.title}</h3>
              <span className="report-type">{report.reportType}</span>
            </div>
            <p className="report-date">
              Uploaded on: {new Date(report.createdAt).toLocaleDateString()}
            </p>
            <a href={report.fileURL} target="_blank" rel="noopener noreferrer" className="report-link">
              View Report
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MyReports;