llm_response = """
Your payment was declined because your card issuer rejected the transaction.
"""

response_check = False

# Basic quality checks

assert llm_response is not None
assert len(llm_response.strip()) > 0

# Check whether the response contains relevant information

keywords = ["payment", "declined", "card"]

for keyword in keywords:
    if str(keyword.lower()) in llm_response.lower():
        print(str(keyword.lower()))
        response_check = True
    else:
        print(str(keyword.lower()))
        response_check = False

if response_check == True:
    print("AI response passed basic quality checks.")
else:
    print("AI response did not pass basic quality checks.")