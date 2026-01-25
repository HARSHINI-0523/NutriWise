const mongoose = require("mongoose");

const LabReportSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
  reportName: String,
  values: {
    hba1c: Number,
    hemoglobin: Number,
    fastingGlucose: Number,
    cholesterol: Number
  },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model("LabReport", LabReportSchema);
