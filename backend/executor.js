const axios = require('axios');
const { GoalModel } = require('./models');

async function triggerN8N(action, input, goalId) {

    await axios.post(process.env.N8N_WEBHOOK_URL, {
        action,
        input,
        goal_id: goalId
    });

    await GoalModel.findByIdAndUpdate(goalId, {
        $push: { logs: `Executed ${action}` }
    });
}

async function executeSteps(goalId) {

    const goal = await GoalModel.findById(goalId);

    for (let step of goal.plan.steps) {
        await triggerN8N(step.action, step.input, goalId);
    }

    await GoalModel.findByIdAndUpdate(goalId, {
        status: "completed",
        result: { message: "All steps triggered" }
    });
}

module.exports = { executeSteps };
