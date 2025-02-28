import openai
from dotenv import load_dotenv
import os
import time
import logging
from datetime import datetime


load_dotenv()

client = openai.OpenAI()
model = 'gpt-4o-mini'
# ## Create a New Assistant - 
# personal_trainer_assis = client.beta.assistants.create(
#     name="Personal Trainer",
#     instructions=""" You are an expert personal personal trainer. 
#                      You help clients in their weightloss to loose fat 
#                      and gain muscles through exercise, diet and yoga.
#                      You help them with their physical and mental health""",
#     model=model
# )
# assistant_id = personal_trainer_assis.id
# print(personal_trainer_assis.id)
# # +++++ Create a Thread to store messages and context +++++ 
# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             "content": """How do I get started with 
#                         working out to loose weight?"""
#         }
#     ],
# )

# thread_id = thread.id
# print(thread_id)

assistant_id= "asst_Rj0XJSKx8v8O36F3MCp53SWQ"
thread_id = "thread_03jHTPFBAEuPNymCSfc6X9vB" 


def wait_for_active_run_to_complete(client, thread_id, sleep_interval=5):
    """Waits until any active run for the thread is completed."""
    while True:
        active_runs = client.beta.threads.runs.list(thread_id=thread_id)
        running = [run for run in active_runs.data if run.status in ("in_progress", "queued")]
        if not running:
            break  # No active runs, safe to proceed
        print("A run is still active. Waiting for it to complete...")
        time.sleep(sleep_interval)

# 1️⃣ **Wait for any active run to complete**
wait_for_active_run_to_complete(client, thread_id)


# +++++ Send a message to the assistant +++++
message = "How do I build strong muscles?"
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content= message
)

# +++++ Run your assistant +++++

run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions="Please address the user as James Bond",
)

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """Waits for the run to complete. Prints the elapsed time.
    :param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: The number of seconds to wait between checks.
    """
    while True:

        try: 
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time))
                print(f"Elapsed time: {formatted_elapsed_time}")
                logging.info(f"Run completed in: {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                if run.status == "completed":
                    messages = client.beta.threads.messages.list(
                        thread_id=thread_id)
                    last_message = messages.data[0]
                    response = last_message.content[0].text.value
                    print(f"Assistant response: {response}")
                    break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info(f"Waiting for run to complete ....")
        time.sleep(sleep_interval)

# === Run ===

wait_for_run_completion(client, thread_id, run.id)

# Steps = Logs = 

run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)

if run_steps.data:
    print(f"Steps---> {run_steps.data[0]}")
else:
    print("No steps found in run_steps data.")
