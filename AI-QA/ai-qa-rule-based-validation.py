response = """
Your refund has been approved.
The amount will be credited within 5 business days.
"""

assert "refund" in response.lower()
assert "5 business days" in response.lower()

