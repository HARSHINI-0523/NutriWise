import mongoose from "mongoose";

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

export default mongoose.model("LabReport", LabReportSchema);
