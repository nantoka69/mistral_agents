from mistralai import Mistral

mistral_api_key = "NvEjm1hksFO8OkiZqfWS4jwLTLQtnsgX"
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
    tools=[{"type": "web_search"}],
    completion_args={
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens
    }
)

response = client.beta.conversations.start(
    agent_id=agent.id,
    inputs="What is today's share price of Alphabet A (GOOG)"
)
print(response.outputs[1].content[0].text)
print(response.outputs[1].content[1].url)

# Output is non-deterministic:
# $209.14
# [TextChunk(text='The share price of Alphabet A (GOOG) is $209.14 as of August 27, 2025', type='text'), ToolReferenceChunk(tool='web_search', title='Mixed options sentiment in Alphabet with shares up 0.57% - TipRanks.com', type='tool_reference', url='https://www.tipranks.com/news/the-fly/mixed-options-sentiment-in-alphabet-with-shares-up-0-57-thefly', favicon='https://imgs.search.brave.com/Fy8mK1OL8AsqdTw9wP8nQlPqSoVi1CnSJLGsrm1tqnU/rs:fit:32:32:1:0/g:ce/aHR0cDovL2Zhdmlj/b25zLnNlYXJjaC5i/cmF2ZS5jb20vaWNv/bnMvODNlNWE3OGM1/YmE3YzAwYTQxZDA3/ZDE2NzZjYWEyOWYy/MWVlMGJkOTA5NmRh/NTQzZDg2OGFmNTRm/ZDZiMTY2NC93d3cu/dGlwcmFua3MuY29t/Lw', description='Mixed options sentiment in Alphabet (GOOG), with shares up $1.19, or 0.57%, <strong>near $209.14</strong>. Options volume relatively light with 43k contracts traded and calls leadin...'), TextChunk(text='.', type='text')]

response = client.beta.conversations.start(
    agent_id=agent.id,
    inputs="Go to https://finance.yahoo.com/quote/GOOG/ and fetch the bid price on that page"
)
print(response.outputs[1].content)
