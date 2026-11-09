context = """
Personal loan interest rate is 8.5%.
Maximum loan tenure is 5 years.
"""

response = """
The maximum loan tenure is 10 years.
"""

expected_value = "5 years"

if expected_value not in response.lower():
    print("Potential hallucination or incorrect answer detected.")
