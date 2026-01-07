const axios = require('axios');
const { GoalModel } = require('./db');

async function processGoal(goal, user_id) {

    // Step 1 – ask ChatGPT to PLAN

    const plannerPrompt = `
You are an AI planner.

User goal: "${goal}"

Respond strictly in JSON format:

{
  "steps": [
     {"action": "tool_name", "input": "description"},
     {"action": "tool_name", "input": "description"}
  ]
}
`;

    const response = await axios.post(
        "https://api.openai.com/v1/chat/completions",
        {
            model: "gpt-4o-mini",
            messages: [
                { role: "system", content: plannerPrompt }
            ]
        },
        {
            headers: {
                Authorization: `Bearer ${process.env.OPENAI_KEY}`
            }
        }
    );

    let plan;
    try {
        plan = JSON.parse(response.data.choices[0].message.content);
    } catch {
        throw new Error("LLM did not return valid JSON plan");
    }

    // Step 2 – save goal with plan

    const goalDoc = await GoalModel.create({
        user_id,
        goal,
        plan,
        status: "planning_complete"
    });

    const goalId = goalDoc._id;

    // Step 3 – EXECUTE tools via n8n

    await executePlanWithN8N(plan.steps, goalId);

    return goalId;
}

async function executePlanWithN8N(steps, goalId) {

    for (let s of steps) {

        // Here you integrate n8n
        // call an existing workflow webhook

        await axios.post(process.env.N8N_WEBHOOK_URL, {
            action: s.action,
            input: s.input,
            goal_id: goalId
        });

        await GoalModel.findByIdAndUpdate(goalId, {
            $push: { logs: `Triggered ${s.action}` }
        });
    }
}
    
module.exports = { processGoal };
