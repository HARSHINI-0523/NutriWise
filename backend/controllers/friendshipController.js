// controllers/friendshipController.js
const Friendship = require("../models/Friendship");
const User = require("../models/User"); // Assuming User model is in this path

// Get all of a user's accepted friends
exports.getFriends = async (req, res) => {
  const { userId } = req.params;
  try {
    const friendships = await Friendship.find({
      $or: [{ requester: userId }, { recipient: userId }],
      status: "accepted",
    })
    .populate("requester", "name email") // Get the requester's details
    .populate("recipient", "name email"); // Get the recipient's details

    // Extract the friend object from the friendship document
    const friends = friendships.map(friendship =>
      friendship.requester._id.toString() === userId ? friendship.recipient : friendship.requester
    );
    res.json(friends);
  } catch (err) {
    res.status(500).json({ message: "Server Error" });
  }
};

// Get all pending requests a user has received
exports.getReceivedRequests = async (req, res) => {
  const { userId } = req.params;
  try {
    const requests = await Friendship.find({
      recipient: userId,
      status: "pending",
    }).populate("requester", "name email"); // We need to know who sent the request
    res.json(requests);
  } catch (err) {
    res.status(500).json({ message: "Server Error" });
  }
};

// Respond to a friend request (accept or reject)
exports.handleRequest = async (req, res) => {
  const { friendshipId } = req.params;
  const { action } = req.body; // The action will be 'accept' or 'reject'

  try {
    // For accepting, we find the request and update its status
    if (action === "accept") {
      const friendship = await Friendship.findByIdAndUpdate(
        friendshipId,
        { status: "accepted" },
        { new: true }
      );
      // Optional: Logic to send a notification to the original requester can be added here
      res.json({ message: "Friend request accepted.", friendship });
    } 
    // For rejecting, we find the request and delete it entirely from the database
    else if (action === "reject") {
      const deletedRequest = await Friendship.findByIdAndDelete(friendshipId);
      res.json({ message: "Friend request rejected.", friendshipId: deletedRequest._id });
    } else {
      res.status(400).json({ message: "Invalid action." });
    }
  } catch (err) {
    res.status(500).json({ message: "Server Error" });
  }
};

// Get friend suggestions (users with mutual friends)
exports.getSuggestions = async (req, res) => {
  const { userId } = req.params;
  try {
    // Step 1: Find the current user's friends
    const friendships = await Friendship.find({
      $or: [{ requester: userId }, { recipient: userId }],
      status: "accepted",
    });
    const friendIds = friendships.map(f =>
      f.requester.toString() === userId ? f.recipient.toString() : f.requester.toString()
    );

    // Step 2: Find "friends of friends"
    const friendsOfFriendsFriendships = await Friendship.find({
      $or: [{ requester: { $in: friendIds } }, { recipient: { $in: friendIds } }],
      status: "accepted",
    });

    const suggestionIds = new Set();
    friendsOfFriendsFriendships.forEach(f => {
      const friendOfFriendId = f.requester.toString() === userId ? f.recipient.toString() : f.requester.toString();
      // Exclude the user and their current friends
      if (friendOfFriendId !== userId && !friendIds.includes(friendOfFriendId)) {
        suggestionIds.add(friendOfFriendId);
      }
    });

    // Step 3: Fetch the user profiles for the suggested IDs
    const suggestions = await User.find({
      _id: { $in: [...suggestionIds] },
    }).select("name email");

    res.json(suggestions);
  } catch (err) {
    res.status(500).json({ message: "Server Error" });
  }
};

exports.sendRequest = async (req, res) => {
  const { requesterId, recipientId } = req.body;

  try {
    // Check if a friendship/request already exists to avoid duplicates
    const existing = await Friendship.findOne({
      $or: [
        { requester: requesterId, recipient: recipientId },
        { requester: recipientId, recipient: requesterId },
      ],
    });

    if (existing) {
      return res.status(400).json({ message: "A friendship or request already exists." });
    }

    const newFriendship = new Friendship({
      requester: requesterId,
      recipient: recipientId,
    });

    await newFriendship.save();
    res.status(201).json({ message: "Friend request sent successfully." });
  } catch (err) {
    console.error("Send request error:", err);
    res.status(500).json({ message: "Server Error" });
  }
};