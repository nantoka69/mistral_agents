import yfinance as yf
from mistralai import Mistral
from mistralai import FunctionResultEntry
import json

mistral_api_key = "..."
client = Mistral(mistral_api_key)

model = "mistral-medium"
temperature=0
top_p=1
max_tokens=1000

def get_current_stock_price(ticker_symbol):
    print(f"Searching stock price for {ticker_symbol} ...")
    try:
        stock_ticker= yf.Ticker(ticker_symbol)
        current_price = stock_ticker.history(period='1d')['Close'].iloc[-1]
        return current_price
    except Exception as e:
        return f"An error occurred: {e}"

def call_function(function_name, arguments_json):
    if function_name == "get_current_stock_price":
        return_value = get_current_stock_price(**json.loads(arguments_json))
    else:
        return_value = f"An error occurred: No function {function_name} available"
    return return_value

stock_price_tool = {
    "type": "function",
    "function": {
        "name": "get_current_stock_price",
        "description": "Retrieve the current price of a stock for a given ticker symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker_symbol": {
                    "type": "string",
                },
            },
            "required": [
                "ticker_symbol",
            ]
        },
    },
}

stock_price_agent = client.beta.agents.create(
    model="mistral-medium",
    description="Can find the current current price of a stock",
    name="stock-price-agent",
    tools=[stock_price_tool],
    completion_args={
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens
    }
)

response = client.beta.conversations.start(
    agent_id=stock_price_agent.id,
    inputs="""
    Get me the stock prices of the stocks of these companies:
    Amazon
    Deutsche Bank
    Bayer
    Volkswagen
    
    For German stocks please use a german ticker symbol.
    If there is more than one type of share for these companies list them all.
    """
)

new_inputs = []

for response_output in response.outputs:
    if response_output.type == "function.call":

        result = call_function(response_output.name, response_output.arguments)

        user_function_calling_entry = FunctionResultEntry(
            tool_call_id=response_output.tool_call_id,
            result=json.dumps(result)
        )

        new_inputs.append(user_function_calling_entry)
    else:
        print(response_output.content)

response = client.beta.conversations.append(
    conversation_id=response.conversation_id,
    inputs=new_inputs
)

response_output = response.outputs[0]
print(response_output.content)
