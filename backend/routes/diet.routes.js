const express = require("express");
const { createDietPlan } = require("../controllers/diet.controller");

const router = express.Router();

router.post("/generate", createDietPlan);

module.exports = router;
