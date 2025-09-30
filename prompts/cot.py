# Example of chain of thought prompting.
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

# We are using google gemini model from openai sdk
client = OpenAI(
    # api_key="AIzaSyB_71b98-uHDjVp0igqvneFgaNfyLdkafg",
    # base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Strictly follow the given JSON output format
    - Only run one step at a time
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times)
    and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    {"step": "START" | "PLAN" | "OUTPUT", "content": "string"}

    Example:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: {"step": "PLAN", "content": "Seems like user is interested in the math problems"}
    PLAN: {"step": "PLAN", "content": "looking at the problem, we should solve this problem using BODMAS method"}
    PLAN: {"step": "PLAN", "content": "Yes, The BODMAS is correct thing to be done here"}
    PLAN: {"step": "PLAN", "content": "first we must multiply 3 * 5 which is 15"}
    PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 15 / 10"}
    PLAN: {"step": "PLAN", "content": "We must perform divide that is 15 / 10 = 1.5"}
    PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 1.5"}
    PLAN: {"step": "PLAN", "content": "Now finally lets perform the add 3.5"}
    PLAN: {"step": "PLAN", "content": "Great, we have solved and finally left with 3.5"}
    OUTPUT: {"step": "OUTPUT", "content": "3.5"}

"""

message_history = [{"role": "system", "content": SYSTEM_PROMPT}]

user_query = input("👉🏻")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=message_history,
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})

    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("🔥", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "PLAN":
        print("🧠", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("🤖", parsed_result.get("content"))
        break


# response = client.chat.completions.create(
#     model="gemini-2.5-flash",
#     response_format={"type": "json_object"},
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {
#             "role": "user",
#             "content": "Hey There, can you explain a + b whole square",
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "steps": "START",
#                     "content": "Hey There, can you explain a + b whole square",
#                 }
#             ),
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "steps": "PLAN",
#                     "content": "The user wants an explanation of the algebraic identity (a+b)^2. I should provide the expansion and a clear explanation of its components and meaning.",
#                 }
#             ),
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "steps": "PLAN",
#                     "content": "First, I'll state the identity (a+b)^2 = a^2 + 2ab + b^2. Then, I will explain what (a+b) whole square means in terms of multiplication.",
#                 }
#             ),
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "steps": "PLAN",
#                     "content": "Next, I will derive the identity by multiplying (a+b) by (a+b) using the distributive property.",
#                 }
#             ),
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "steps": "PLAN",
#                     "content": "I will multiply out (a+b) * (a+b) step-by-step: a*(a+b) + b*(a+b).",
#                 }
#             ),
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {"steps": "PLAN", "content": "Then expand to a*a + a*b + b*a + b*b."}
#             ),
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "steps": "PLAN",
#                     "content": "Simplify the terms: a*a becomes a^2, b*b becomes b^2, and a*b + b*a combines to 2ab.",
#                 }
#             ),
#         },
#         {
#             "role": "assistant",
#             "content": json.dumps(
#                 {
#                     "steps": "PLAN",
#                     "content": "Finally, I will combine all the simplified terms to present the full identity (a+b)^2 = a^2 + 2ab + b^2 and provide a brief explanation of each term.",
#                 }
#             ),
#         },
#     ],
# )

# print(response.choices[0].message.content)
