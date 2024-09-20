import time
from utils import *
from openai import OpenAI
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

OPEN_API_KEY = os.environ['OPEN_API_KEY']
ASSISTANT_ID = os.environ['ASSISTANT_ID']

client: OpenAI = OpenAI(api_key=OPEN_API_KEY)
thread = client.beta.threads.create()
assistant = client.beta.assistants.retrieve(assistant_id=ASSISTANT_ID)


# Chatbot logic function using get_completion
def chat_with_bot(prompt):

    # Loading the list of runs in the assistant
    runs = client.beta.threads.runs.list(thread_id=thread.id)

    #  Checking for any incomplete runs
    incomplete_run = [i for i in runs.data if i.status != 'completed']

    # If there is any incomplete run
    if len(incomplete_run) == 0:

        # Create the new message for the user
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )

        # Run the assistant
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="output the response in html formatted way in div tag format"
        )

    else:
        run = incomplete_run[0]

    if run.status == "requires_action":
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        tool_outputs = []

        try:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name in available_functions:
                    function_to_call = available_functions[function_name]
                    output = function_to_call(**function_args)
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": output,
                    })

            # Submit tool outputs and update the run
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

            # Wait for the correct response time
            while run.status in ["in_progress", "queued"]:
                time.sleep(5)
                run = client.beta.threads.runs.retrieve(
                    run_id=run.id,
                    thread_id=thread.id
                )

        except Exception as e:
            return str(e)

    # if run.status == "requires_action":
    #     chat_with_bot(prompt)

    if run.status == "completed":
        # List the messages to get the response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_massages = [i.content[0].text.value for i in messages.data if i.role == 'assistant']
        return assistant_massages[0]
        # for message in messages.data:
        #     if message.role == "assistant":
        #         message_content = message.content[0].text.value
        #         return message_content

    elif run.status == "failed":
        return "Run failed please refresh"

    elif run.status in ["in_progress", "queued"]:
        print(f"Run is {run.status}. Waiting...")
        time.sleep(5)  # Wait for 5 seconds before checking again
    else:
        return f"Unexpected status: {run.status} Check your net or refresh"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    user_input = data.get('user_input')
    bot_response = chat_with_bot(f"{user_input}")
    return jsonify({'response': bot_response})


if __name__ == '__main__':
    app.run(debug=True)
