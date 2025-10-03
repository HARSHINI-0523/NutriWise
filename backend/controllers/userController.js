// In controllers/userController.js
const User = require("../models/User");
const mongoose = require("mongoose");

exports.searchUsers = async (req, res) => {
  const { query } = req.query;
  const { userId } = req.params;

  if (!query) {
    return res.json([]);
  }

  try {
    // This query uses the external search index. It does not depend on any User model changes.
    const users = await User.aggregate([
      {
        $search: {
          index: "user_search_index", // The name of the index you just created
          autocomplete: {
            query: query,
            path: "name", // We're targeting the 'name' field for the search
            fuzzy: {
              maxEdits: 1,      // Allows for one character typo/difference
              prefixLength: 2,  // The first 2 characters must be correct
            },
          },
        },
      },
      {
        $match: {
          _id: { $ne: new mongoose.Types.ObjectId(userId) },
        },
      },
      { $limit: 10 },
      {
        $project: { name: 1, email: 1, _id: 1 },
      },
    ]);

    res.json(users);
  } catch (err) {
    console.error("Search error:", err);
    res.status(500).json({ message: "Server Error" });
  }
};