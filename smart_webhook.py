
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

PROMPT = """
You are an intelligent planner helping the user organize their daily tasks using SMART goals.

Here are today's tasks:
{tasks}

Please:
1. Categorize each task under SMART goals (Spiritual, School, Career, etc.)
2. Assign a priority (High/Medium/Low)
3. Organize into 25-minute Pomodoro blocks between 10:00 AM and 2:30 PM
4. Return JSON with:
   - title
   - goal
   - priority
   - start_time
   - end_time
"""

@app.route('/plan', methods=['POST'])
def plan():
    data = request.get_json()
    task_text = data.get("tasks", "")
    full_prompt = PROMPT.format(tasks=task_text)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": full_prompt}]
    )

    result = response.choices[0].message['content']
    return jsonify({"response": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
