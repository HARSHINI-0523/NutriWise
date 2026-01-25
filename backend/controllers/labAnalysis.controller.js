const Report = require("../models/Report");
const { analyzeLab } = require("../services/python.service");

exports.runLabAnalysis = async (req, res) => {
  try {
    const { reportId } = req.params;

    const report = await Report.findById(reportId);
    if (!report) return res.status(404).json({ msg: "Report not found" });

    const result = await analyzeLab(report.fileURL, report.reportType);


    report.values = result.values;
    report.analysis = result.analysis;

    await report.save();

    res.json({
      msg: "Lab values extracted successfully",
      values: report.values,
      analysis: result.analysis
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ msg: "Analysis failed" });
  }
};
