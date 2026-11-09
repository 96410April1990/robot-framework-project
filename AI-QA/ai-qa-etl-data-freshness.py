def test_data_freshness():
    ingestion_delay_minutes = 42

    assert ingestion_delay_minutes <= 30

test_data_freshness()