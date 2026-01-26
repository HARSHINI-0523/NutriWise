const express = require("express");
const router = express.Router();
const Challenge = require("../models/Challenge");
const User = require("../models/User");
const { protect } = require('../middleware/authMiddleware');
const UserDetails = require("../models/UserDetails");
const Friendship = require("../models/Friendship");

// GET /api/challenges - Get all challenges with completion status for current user (Personalized)
router.get("/", protect, async (req, res) => {
    try {
        const user = req.user;

        // Fetch user details to get conditions
        // Fetch user details to get conditions
        const details = await UserDetails.findById(user._id);

        if (!details) {
            return res.status(400).json({
                error: "PROFILE_MISSING",
                message: "Please fill out the User Details form to unlock personalized challenges."
            });
        }

        let conditions = ['General'];
        if (details.isDiabetic) conditions.push('Diabetic');
        if (details.hasHypertension) conditions.push('Hypertension');
        if (details.hasThyroid) conditions.push('Thyroid');
        if (details.hasHeartDisease) conditions.push('Heart Disease');
        if (details.hasKidneyDisease) conditions.push('Kidney Disease');

        const challenges = await Challenge.find({
            condition: { $in: conditions }
        });
        const today = new Date().toISOString().split('T')[0];

        const getSeed = (str) => {
            let hash = 0;
            for (let i = 0; i < str.length; i++) {
                const char = str.charCodeAt(i);
                hash = (hash << 5) - hash + char;
                hash = hash & hash;
            }
            return Math.abs(hash);
        };

        const dailySeed = getSeed(today);

        const seededRandom = (seed) => {
            let value = seed;
            return function () {
                value = (value * 9301 + 49297) % 233280;
                return value / 233280;
            }
        };

        const randomGen = seededRandom(dailySeed);

        const shuffledChallenges = challenges.sort(() => randomGen() - 0.5);

        const dailyChallenges = shuffledChallenges.slice(0, 5);

        const challengesWithStatus = dailyChallenges.map((challenge) => {
            const isCompleted = user.completedChallenges.includes(challenge._id);
            const isJoined = user.joinedChallenges?.includes(challenge._id);
            return {
                ...challenge.toObject(),
                completed: isCompleted,
                joined: isJoined || isCompleted // If completed, it's implied joined
            };
        });

        res.json(challengesWithStatus);

    } catch (error) {
        console.error("Error fetching challenges:", error);
        res.status(500).json({ message: "Server error" });
    }
});

// PATCH /api/challenges/:id/complete
router.patch("/:id/complete", protect, async (req, res) => {
    try {
        const challengeId = req.params.id;
        const user = await User.findById(req.user._id);

        if (user.completedChallenges.includes(challengeId)) {
            return res.status(400).json({ message: "Challenge already completed" });
        }

        user.completedChallenges.push(challengeId);
        await user.save();

        res.json({ message: "Challenge completed! 🎉" });

    } catch (error) {
        console.error("Error completing challenge:", error);
        res.status(500).json({ message: "Server error" });
    }
});

// POST /api/challenges/:id/join
router.post("/:id/join", protect, async (req, res) => {
    try {
        const challengeId = req.params.id;
        const user = await User.findById(req.user._id);

        if (user.joinedChallenges.includes(challengeId)) {
            return res.status(400).json({ message: "Challenge already joined" });
        }

        user.joinedChallenges.push(challengeId);
        await user.save();

        res.json({ message: "Challenge joined! Let's do this! 🚀" });

    } catch (error) {
        console.error("Error joining challenge:", error);
        res.status(500).json({ message: "Server error" });
    }
});

// GET /api/challenges/social/leaderboard
router.get("/social/leaderboard", protect, async (req, res) => {
    try {
        const userId = req.user._id;

        // 1. Find all accepted friendships
        const friendships = await Friendship.find({
            $or: [{ requester: userId }, { recipient: userId }],
            status: "accepted",
        });

        // 2. Get friend IDs
        const friendIds = friendships.map(f =>
            f.requester.toString() === userId.toString() ? f.recipient : f.requester
        );

        // 3. Find friends' details and their completed challenges
        const friends = await User.find({ _id: { $in: friendIds } })
            .select('name email completedChallenges');

        // 4. Structure the data: Map challengeIDs to list of friends who completed it
        // Since we don't know *which* challenges are being asked about (the frontend has the daily list),
        // we'll just return a map of { challengeId: [friendName1, friendName2] }

        const leaderboard = {};

        friends.forEach(friend => {
            friend.completedChallenges.forEach(challengeId => {
                if (!leaderboard[challengeId]) {
                    leaderboard[challengeId] = [];
                }
                leaderboard[challengeId].push(friend.name);
            });
        });

        res.json(leaderboard);

    } catch (error) {
        console.error("Error fetching leaderboard:", error);
        res.status(500).json({ message: "Server error" });
    }
});

module.exports = router;
