const express = require("express");
const router = express.Router();
const UserDetails = require("../models/UserDetails");

// POST: Save user details
router.post("/", async (req, res) => {
  try {
    const newDetails = new UserDetails(req.body);
    await newDetails.save();
    res.status(201).json({ message: "Details saved successfully!" });
  } catch (error) {
    console.error("Error saving details:", error);
    res.status(500).json({ message: "Failed to save details. Please try again." });
  }
});

// GET: Fetch all user details
router.get("/", async (req, res) => {
  try {
    const allDetails = await UserDetails.find();
    res.json(allDetails);
  } catch (error) {
    console.error("Error fetching details:", error);
    res.status(500).json({ message: "Failed to fetch details." });
  }
});

module.exports = router;
