const LabReport = require("../models/LabReport");
const UserDetails = require("../models/UserDetails");
const DietPlan = require("../models/DietPlan");
const { generateDietPlan } = require("../services/python.service");

exports.createDietPlan = async (req, res) => {
  try {
    const { userId, labReportId } = req.body;

    const labReport = await LabReport.findById(labReportId);
    const userDetails = await UserDetails.findOne({ _id: userId });

    if (!labReport || !userDetails) {
      return res.status(404).json({ message: "Required data not found" });
    }

    const conditions = [];
    if (userDetails.isDiabetic) conditions.push("diabetes");
    if (userDetails.hasHypertension) conditions.push("hypertension");
    if (userDetails.hasThyroid) conditions.push("thyroid");
    if (userDetails.hasHeartDisease) conditions.push("heart_disease");
    if (userDetails.hasKidneyDisease) conditions.push("kidney_disease");

    const payload = {
      conditions,
      lab_values: labReport.values,
      calorie_target: 1800
    };

    const result = await generateDietPlan(payload);

    const savedPlan = await DietPlan.create({
      userId,
      labReportId,
      plan: result.meal_plan,
      avoidList: result.avoid_list
    });

    res.json(savedPlan);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Diet plan generation failed" });
  }
};
