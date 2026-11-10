import pytest
from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import GEval
from deepeval.models import GeminiModel
from deepeval.test_case import LLMTestCase, SingleTurnParams

load_dotenv()

gemini = GeminiModel(
    model="gemini-3.5-flash-lite"
)

dataset = EvaluationDataset()
dataset.test_cases = [
    LLMTestCase(
        input="What is Selenium?",
        actual_output="Selenium automates web browsers.",
        expected_output="Selenium is a browser automation framework.",
    ),
    LLMTestCase(
        input="What is Pytest?",
        actual_output="Pytest is a Python testing framework.",
        expected_output="Pytest is used for testing Python applications.",
    ),
    LLMTestCase(
        input="What is Playwright?",
        actual_output="Playwright automates web browsers.",
        expected_output="Playwright is a browser automation framework.",
    ),
]

@pytest.mark.parametrize(
    "test_case",
    dataset.test_cases,
    ids=[test_case.input for test_case in dataset.test_cases],
)
def test_golden_dataset(test_case):
    metric = GEval(
        name="answer correctness",
        criteria=(
            "Judge whether the actual output correctly answers the input "
            "and conveys the same essential information as the expected output."
        ),
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.EXPECTED_OUTPUT,
        ],
        threshold=0.7,
        model=gemini
    )
    
    assert_test(test_case, [metric])
