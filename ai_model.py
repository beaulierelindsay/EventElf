from openai import OpenAI
from config.config import API_KEY


# # def parse_event_details(user_input):
# response = openai.ChatCompletion.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "hi, how are you?"}]
#     # messages=[{"role": "user", "content": user_input}]
# )
#     # return response["choices"][0]["message"]["content"]

client = OpenAI(api_key=API_KEY)

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "developer", "content": "You are a friendly AI and answer in only 5 words or less."},
        {
            "role": "user",
            "content": "how are you?"
        }
    ]
)

print(completion.choices[0].message.content)
# print(completion.choices[0])
# print(completion)