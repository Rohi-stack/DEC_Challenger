const mongoose = require('mongoose');

const GoalSchema = new mongoose.Schema({
    user_id: String,
    goal_text: String,
    plan: Object,
    status: String,
    logs: [String],
    result: Object,
    created_at: {
        type: Date,
        default: Date.now
    }
});

const GoalModel = mongoose.model("Goal", GoalSchema);

module.exports = { GoalModel };
