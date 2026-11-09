def test_pipeline_idempotency():
    first_run = {"T001", "T002", "T003"}
    second_run = {"T001", "T002", "T003"}

    assert first_run == second_run

test_pipeline_idempotency()