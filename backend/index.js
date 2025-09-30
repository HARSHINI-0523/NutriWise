// index.js
const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const dotenv=require("dotenv");
const mongoose = require("mongoose");
dotenv.config();
const app = express();
PORT=process.env.PORT||5000;

//Import routes
const authRouter = require("./routes/auth");
const reportRoutes = require('./routes/reportRoutes');

// Middleware
app.use(cors());
app.use(bodyParser.json());

//Use routes
app.use("/api/auth", authRouter);
app.use('/api/reports', reportRoutes);

// MongoDB Connection
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log("MongoDB connected"))
.catch((err) => console.error("MongoDB connection error:", err));

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
