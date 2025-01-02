import json
import os
import boto3
from dotenv import load_dotenv
import streamlit as st
import fmpsdk

load_dotenv()

# Initialize AWS Bedrock client (for model interactions, if needed)
modelId = 'anthropic.claude-3-sonnet-20240229-v1:0'
api_key = os.getenv("FINANCIAL_MODELING_PREP_API_KEY")
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1',
)

toolConfig = {'tools': [], 'toolChoice': {'auto': {}}}

# Define the ToolsList class with tool functions
class ToolsList:
    def get_stock_price(self, symbol: str):
        """
        Fetch the current stock price and other relevant data for the given symbol.
        Uses the fmpsdk to fetch stock quote data.
        """
        try:
            # Fetch stock data using fmpsdk quote
            stock = fmpsdk.quote(apikey=api_key, symbol=symbol)
            
            # Extract the first item from the list (stock data)
            if stock:
                stock = stock[0]
                return json.dumps(stock)
            else:
                return {"error": f"No data found for symbol: {symbol}"}

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

    def get_company_financials(self, symbol):
        try:
            # Fetch stock data using fmpsdk quote
            financials = fmpsdk.company_profile(apikey=api_key, symbol=symbol)
            
            # Extract the first item from the list (stock data)
            if financials:
                financials = financials[0]
                return json.dumps(financials)
            else:
                return {"error": f"No data found for symbol: {symbol}"}

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}


    def get_income_statement(self, symbol):
        try:
            # Fetch stock data using fmpsdk quote
            stock = fmpsdk.income_statement(apikey=api_key, symbol=symbol)
            
            # Extract the first item from the list (stock data)
            if stock:
                stock = stock[0]
                return json.dumps(stock)
            else:
                return {"error": f"No data found for symbol: {symbol}"}

        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
    
# Tool Configuration
toolConfig['tools'].append({
    'toolSpec': {
        'name': 'get_stock_price',
        'description': 'Get the current stock price for a given company symbol.',
        'inputSchema': {
            'json': {
                'type': 'object',
                'properties': {
                    'symbol': {
                        'type': 'string',
                        'description': 'The stock ticker symbol, e.g., AAPL for Apple.'
                    }
                },
                'required': ['symbol']
            }
        }
    }
})


toolConfig['tools'].append({
    'toolSpec': {
        'name': 'get_company_financials',
        'description': 'Get basic financial information for a given company.',
        'inputSchema': {
            'json': {
                'type': 'object',
                'properties': {
                    'symbol': {
                        'type': 'string',
                        'description': 'The stock ticker symbol, e.g., GOOGL for Alphabet Inc.'
                    }
                },
                'required': ['symbol']
            }
        }
    }
})



toolConfig['tools'].append({
    'toolSpec': {
        'name': 'get_income_statement',
        'description': 'Get the last income statement for a given company symbol.',
        'inputSchema': {
            'json': {
                'type': 'object',
                'properties': {
                    'symbol': {
                        'type': 'string',
                        'description': 'The stock ticker symbol, e.g., AMZN for Amazon.'
                    }
                },
                'required': ['symbol']
            }
        }
    }
})

# Function for orchestrating the conversation flow
def converse(prompt, system=''):
    # Add the initial prompt:
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "text": prompt
                }
            ]
        }
    ]
    
    print(f"Initial prompt:\n{json.dumps(messages, indent=2)}")

    # Invoke the model the first time
    output = converse_with_tools(messages, system)
    print(f"Output so far:\n{json.dumps(output['output'], indent=2, ensure_ascii=False)}")

    # Add the intermediate output to the prompt:
    messages.append(output['output']['message'])

    # Check if function calling is triggered
    function_calling = next((c['toolUse'] for c in output['output']['message']['content'] if 'toolUse' in c), None)

    if function_calling:
        # Get the tool name and arguments
        tool_name = function_calling['name']
        tool_args = function_calling['input'] or {}

        # Run the tool
        print(f"Running ({tool_name}) tool...")
        print("tool_args:", tool_args)
        print(f"Calling {tool_name} with arguments {tool_args}")

        # Run the tool with the symbol argument
        tool_response = getattr(ToolsList(), tool_name)(tool_args['symbol'])
        tool_status = 'success' if tool_response else 'error'

        # Add the tool result to the prompt
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        'toolResult': {
                            'toolUseId': function_calling['toolUseId'],
                            'content': [
                                {
                                    "text": tool_response
                                }
                            ],
                            'status': tool_status
                        }
                    }
                ]
            }
        )

        # Invoke the model one more time to finalize the conversation
        output = converse_with_tools(messages, system)
        print(f"Final output:\n{json.dumps(output['output'], indent=2, ensure_ascii=False)}\n")

    return output['output']


# Function for calling the Bedrock Converse API
def converse_with_tools(messages, system='', toolConfig=toolConfig):
    response = bedrock.converse(
        modelId=modelId,
        system=system,
        messages=messages,
        toolConfig=toolConfig
    )
    return response

def chat_app():
    st.title("Market Assistant")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        system_message = [{"text": "You're provided with tools that can fetch the current stock price for a given company symbol ('get_stock_price'), basic financial information for a given company ('get_company_financials'), and the last income statement for a company ('get_income_statement'). \
                Use these tools if necessary to answer the question. Do not mention the tools in your final answer."}]
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Get assistant response from the bot
        response = converse(prompt=prompt, system=system_message).get("message", {}).get("content", [{}])[0].get("text", "No response received.")

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)

if __name__ == "__main__":
    chat_app()