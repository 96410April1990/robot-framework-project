def test_total_amount():
    amount = 1000
    tax = 180
    actual_amount = 1180

    expected_total = amount + tax

    assert actual_amount == expected_total