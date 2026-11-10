from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.models import GeminiModel
from deepeval.metrics import FaithfulnessMetric
from deepeval.test_case import LLMTestCase

load_dotenv()

gemini = GeminiModel(
    model="gemini-3.5-flash-lite"
)

def test_faithfulness_negative():
    test_case = LLMTestCase(
        input="What is the savings account interest rate?",
        actual_output=(
            "The savings account offers 8% annual interest."
        ),
        retrieval_context=[
            "The savings account offers 4% annual interest."
        ]
    )

    metric = FaithfulnessMetric(
        threshold=0.7,
        model=gemini,
        include_reason=True
    )

    assert_test(test_case, [metric])

def test_faithfulness_positive():
    test_case = LLMTestCase(
        input="What is the savings account interest rate?",
        actual_output=(
            "The savings account offers 4% annual interest."
        ),
        retrieval_context=[
            "The savings account offers 4% annual interest."
        ]
    )

    metric = FaithfulnessMetric(
        threshold=0.7,
        model=gemini,
        include_reason=True
    )

    assert_test(test_case, [metric])