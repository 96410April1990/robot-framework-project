import json

# Examples for basic validation
response = "Your refund will be processed within 5 business days."

assert response
assert len(response.strip()) < 500

response_one = '{"status": "approved", "amount": 500}'
data = json.loads(response_one)

assert "status" in data
assert "amount" in data
assert isinstance(data["status"], str)
assert isinstance(data["amount"], int)

