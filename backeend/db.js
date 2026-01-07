const mongoose = require('mongoose');

async function connectDB() {
    await mongoose.connect(process.env.MONGO_URI);
    console.log("Database connected");
}

const GoalSchema = new mongoose.Schema({
    user_id: String,
    goal: String,
    plan: Object,
    logs: [String],
    result: Object,
    status: String
});

const GoalModel = mongoose.model("Goal", GoalSchema);

module.exports = { connectDB, GoalModel };
