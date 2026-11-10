from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.models import GeminiModel
from deepeval.metrics import (
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric
)
from deepeval.test_case import LLMTestCase

load_dotenv()

gemini = GeminiModel(
    model="gemini-3.5-flash-lite"
)

def test_rag_retrieval():
    test_case = LLMTestCase(
        input="What is the company's leave policy?",

        actual_output=(
            "Employees receive 20 annual leave days "
            "and 10 sick leave days."
        ),

        expected_output=(
            "Employees receive 20 annual leave days "
            "and 10 sick leave days."
        ),

        retrieval_context=[
            "Employees receive 20 annual leave days.",
            "Employees receive 10 sick leave days."
        ]
    )

    metrics = [
        ContextualPrecisionMetric(
            threshold=0.7,
            model=gemini
        ),
        ContextualRecallMetric(
            threshold=0.7,
            model=gemini
        ),
        ContextualRelevancyMetric(
            threshold=0.7,
            model=gemini
        )
    ]

    assert_test(test_case, metrics)