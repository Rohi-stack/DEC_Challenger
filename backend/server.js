require('dotenv').config();
const express = require('express');
const cors = require('cors');

const { connectDB } = require('./db');
const { processGoal } = require('./agent');
const { executeSteps } = require('./executor');

const app = express();

app.use(cors());
app.use(express.json());

connectDB();

app.post('/goal', async (req, res) => {

    const { goal, user_id } = req.body;

    const goalId = await processGoal(goal, user_id);

    // fire and forget execution
    executeSteps(goalId);

    res.json({
        goal_id: goalId
    });
});

app.get('/status/:id', async (req, res) => {

    const id = req.params.id;

    const goal = await GoalModel.findById(id);

    res.json({
        status: goal.status,
        logs: goal.logs,
        result: goal.result
    });
});

app.listen(3000, () => {
    console.log("Agent backend running on http://localhost:3000");
});
