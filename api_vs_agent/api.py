from mistralai import Mistral

mistral_api_key = "..."
client = Mistral(api_key=mistral_api_key)

model = "mistral-medium"
temperature=0
top_p=1
max_tokens=1000

def call_mistral_api(prompt):
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Only answer, not explanations.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens
    )

    print(prompt)
    print(chat_response.choices[0].message.content)


call_mistral_api("Translate into German: mistral.ai is a great tool.")
call_mistral_api("And now translate it into French.")

call_mistral_api("What is today's share price of Alphabet A (GOOG)")

