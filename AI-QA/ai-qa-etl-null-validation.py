def test_mandatory_fields():
    record = {
        "customer_id": "C001",
        "amount": 500,
        "transaction_date": None
    }

    assert record["customer_id"] is not None
    assert record["amount"] is not None
    assert record["transaction_date"] is not None

test_mandatory_fields()