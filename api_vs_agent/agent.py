from mistralai import Mistral

mistral_api_key = "..."
client = Mistral(mistral_api_key)

model = "mistral-medium"
temperature=0
top_p=1
max_tokens=1000

agent = client.beta.agents.create(
    model=model,
    description="A simple Agent.",
    name="Simple Agent",
    instructions="Only answer, not explanations.",
    completion_args={
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens
    }
)

response = client.beta.conversations.start(
    agent_id=agent.id,
    inputs="Translate into German: mistral.ai is a great tool."
)
print(response.outputs[0].content)

response = client.beta.conversations.append(
    conversation_id=response.conversation_id,
    inputs="And now translate it into French."
)
print(response.outputs[0].content)

response = client.beta.conversations.start(
    agent_id=agent.id,
    inputs="What is today's share price of Alphabet A (GOOG)"
)
print(response.outputs[0].content)
