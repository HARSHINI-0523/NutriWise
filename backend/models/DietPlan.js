import mongoose from "mongoose";

const DietPlanSchema = new mongoose.Schema({
  userId: mongoose.Schema.Types.ObjectId,
  labReportId: mongoose.Schema.Types.ObjectId,
  plan: Object, // 7-day plan JSON
  avoidList: [String],
  createdAt: { type: Date, default: Date.now }
});

export default mongoose.model("DietPlan", DietPlanSchema);
