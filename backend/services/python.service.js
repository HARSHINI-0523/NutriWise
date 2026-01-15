const axios = require("axios");

exports.generateDietPlan = async (payload) => {
  const response = await axios.post(
    "http://localhost:8000/generate",
    payload
  );
  return response.data;
};
