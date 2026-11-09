def test_schema():

    expected_columns = {
        "customer_id",
        "amount",
        "transaction_date"
    }

    actual_columns = {
        "customer_id",
        "amount",
        "transaction_date",
        "currency"
    }

    assert actual_columns == expected_columns

test_schema()