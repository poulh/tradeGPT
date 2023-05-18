import os
import openai

# Set up your OpenAI API key
# echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc
# Run Menu > Edit Configurations
openai.api_key = os.environ["OPENAI_API_KEY"]

# Generate a response from the OpenAI API
def chat(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.0, # deterministic
    )

    return response.choices[0].message.content.strip()


def ask(prompt):

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        # message = prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the generated problem from the API response
    return response.choices[0].text.strip()

def create_embeddings(prompt):
    # Generate embedding using OpnAI API
    response = openai.Embedding.create(
      engine="text-curie-001",
      prompt=prompt,
    )

    return response['data'][0]['embedding']

# todo: there has to be a way to access the previous messages from the ChatCompletion
# todo: these prompts are not working as well as I would like. i occasionally get back text plus the JSON string
# todo: JSON keys are not always consistent
chat_messages = [
            {"role": "system", "content": "You are a helpful assistant in the finance industry"},
            {"role": "system", "content": "The only possible order types are buy, sell, and sell short and will be the first word entered as b s and ss"},
            {"role": "system","content": "The symbol can be entered uppercase or lower case.  always  convert the symbol to uppercase."},
            {"role": "system", "content": "include both the symbol and the reuters ric code in the response"},
            {"role": "user", "content": "s AAPL 3000  @475.67"},
            {"role": "assistant", "content": "Sell 3000 shares of AAPL at price 475.67"},
            {"role": "user", "content": "b IBM 200  @ 5.63"},
            {"role": "assistant", "content": "Buy 200 shares of IBM at price 5.63"},
            {"role": "user", "content": "ss MSFT 45000  @ 145.63"},
            {"role": "assistant", "content": "Sell short 45000 shares of MSFT at price 145.63"},
            {"role": "user", "content": "ss DDOG 800 123.45"},
            {"role": "assistant", "content": "Sell short 800 shares of DDOG at price 123.45"},
            {"role": "system", "content": "only return the response  is JSON and include the sentence as part of the JSON string"},

]

while True:
    # Ask the user to enter a prompt
    prompt = input(f"Ask a question. (Type 'quit' to exit) ")

    # If the user entered "quit", break out of the loop
    if prompt.lower() == "quit":
        break

    chat_messages.append({"role": "user", "content": prompt})
    print(chat(chat_messages))

