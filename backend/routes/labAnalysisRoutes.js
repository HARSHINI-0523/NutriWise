const express = require("express");
const router = express.Router();
const Report = require("../models/Report");
const { protect } = require("../middleware/authMiddleware");
const axios = require("axios");
const fs = require("fs");
const { spawnSync } = require("child_process");
const path = require("path");
const { generateMedicalAnalysis } = require("../utils/groqClient");
const TMP_DIR = path.join(__dirname, "../tmp");
if (!fs.existsSync(TMP_DIR)) fs.mkdirSync(TMP_DIR);

router.get("/process/:id", protect, async (req, res) => {
  try {
    const report = await Report.findById(req.params.id);
    if (!report) return res.status(404).json({ msg: "Report not found" });
    if (report.uploadedBy.toString() !== req.user.id)
      return res.status(403).json({ msg: "Unauthorized" });

    // --- DOWNLOAD FILE ---
    const filePath = path.join(TMP_DIR, `${report._id}.png`);
    const response = await axios.get(report.fileURL, { responseType: "arraybuffer" });
    fs.writeFileSync(filePath, response.data);

    // --- CALL PYTHON ---
    const py = spawnSync("python", [
      "lab_report_analysis/run_analysis.py",
      filePath,
    ]);

    const stdout = py.stdout.toString().trim();
    const stderr = py.stderr.toString().trim();

    if (stderr) console.log("PY STDERR:", stderr);
    console.log("PY STDOUT:", stdout);

    let output;
    try {
      output = JSON.parse(stdout);
    } catch (jsonErr) {
      return res.status(500).json({
        msg: "Python returned invalid JSON",
        raw: stdout,
      });
    }

    if (output.error) {
      return res.status(500).json({
        msg: "Analysis failed",
        pythonError: output.error,
      });
    }

    // --- SAVE RESULTS ---
    report.values = output.extracted_data || {};

    const aiSummary = await generateMedicalAnalysis(report.values);

    report.analysis = aiSummary; // save plain text summary
    await report.save();

    res.json({ msg: "Analysis completed", report });

  } catch (err) {
    console.error(err);
    res.status(500).json({ msg: "Server error", error: err.message });
  }
});

module.exports = router;
