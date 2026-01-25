const axios = require("axios");

exports.generateDietPlan = async (payload) => {
  const response = await axios.post(
    "http://127.0.0.1:8000/generate",
    payload
  );
  return response.data;
};

exports.analyzeLab = async (fileURL, reportType) => {
  const res = await axios.post("http://127.0.0.1:9000/analyze", {
    file_url: fileURL,
    report_type: reportType
  });
  return res.data;
};