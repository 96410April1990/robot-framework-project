def test_customer_references():
    customers = {"C001", "C002", "C003"}

    transaction_customer_ids = ["C001", "C002", "C999"]

    for customer_id in transaction_customer_ids:
        assert customer_id in customers

test_customer_references()