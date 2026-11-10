company_policy = """
Employees receive 20 days of annual leave.
"""

response = """
Employees receive 20 days of annual leave and 10 days of sick leave.
"""

assert "20 days" in response.strip()

#Potential unsupported claim or hallucination:
if "10 days of sick leave." in response.lower():
    print("Potential hallucination detected.")
