
![market-assistant](https://github.com/user-attachments/assets/60209de5-6e3d-4e27-86eb-b4f0a9c74400)

**Market Assistant: Stock and Financial Data Chatbot**

This is a market data assistant application built using Streamlit, AWS Bedrock Converse, FMPSDK, and other supporting libraries. The chatbot leverages Anthropic Claude Sonnet model and interacts with financial data APIs to provide real time stock prices, financials, and income statements for various companies.

**Features**

-   Real-time Stock Price: Fetch the current stock price of a given symbol (e.g., AAPL for Apple).
-   Company Financial Information: Get basic financial details for a specific company.
-   Income Statement: Retrieve the latest income statement of a company.

**Prerequisites**

Before running the code, make sure to complete the following:

-   [AWS CLI Setup](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) : Install and configure the AWS Command Line Interface (CLI) with the appropriate credentials.

-   AWS Bedrock Access: You must have access to Amazon Bedrock and the appropriate credentials to use its models, including the Anthropic Claude Sonnet model.

-   Financial Modelling Prep Setup: You need to have a valid financialmodelingprep API key to access the real time financial data. You can get it from [financialmodelingprep](https://site.financialmodelingprep.com/)

**Setup**

1. Clone the Repository

    ```
    git clone https://github.com/stackmodel/market-assistant.git
    cd market-assistant
    ```
2. Rename .env.example to .env file in the root of your project to store your financialmodelingprep api key.

    ```FINANCIAL_MODELING_PREP_API_KEY=your_api_key_here```
3. Make sure you have Python 3.12 or higher installed. Then, create a virtual environment and install the dependencies:
    
    ```python3 -m venv venv```

4. Run the following to install the necessary dependencies:
    ```
    source venv/bin/activate
    pip install -r requirements.txt 
    ```
5. To run the Streamlit app locally, simply execute:

    ```streamlit run app.py```

Once the app is running, enter http://localhost:8501 in your browser to load the streamlit app.


**Enter a query such as:**

-   "What is the stock price of AAPL?"
-   "Show me the financials of Microsoft."
-   "Give me the income statement for Amazon."

The assistant will process the input and provide the appropriate response, fetching data from the APIs as needed.




