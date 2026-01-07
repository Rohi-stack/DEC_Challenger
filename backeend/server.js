require('dotenv').config();
const express = require('express');
const cors = require('cors');

const { processGoal } = require('./agent');
const { connectDB } = require('./db');

const app = express();

app.use(cors());
app.use(express.json());

connectDB();

app.post('/goal', async (req, res) => {
    try {
        const { goal, user_id } = req.body;

        const goalId = await processGoal(goal, user_id);

        res.json({
            status: "accepted",
            goal_id: goalId
        });

    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.get('/status/:id', async (req, res) => {
    const id = req.params.id;
    res.json({ message: "fetch status from DB for " + id });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log("Backend running on port " + PORT);
});
