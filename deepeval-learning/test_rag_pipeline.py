import pytest
from deepeval import assert_test
from deepeval.dataset import EvaluationDataset, Golden
from deepeval.models import GeminiModel
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric
)
from deepeval.test_case import LLMTestCase
from rag_application import ask_hr_bot

gemini = GeminiModel(
    model="gemini-3.5-flash-lite"
)

dataset = EvaluationDataset(
    goldens=[
        Golden(
            input="How many annual leave days do employees get?",
            expected_output="Employees receive 20 annual leave days."
        ),
        Golden(
            input="How many sick leave days do employees get?",
            expected_output="Employees receive 10 sick leave days."
        ),
        Golden(
            input="What is the remote work policy?",
            expected_output="Employees can work remotely 2 days per week."
        )
    ]
)

@pytest.mark.parametrize("golden", dataset.goldens)
def test_hr_chatbot(golden):
    actual_output, documents = ask_hr_bot(
        golden.input
    )

    test_case = LLMTestCase(
        input=golden.input,
        actual_output=actual_output,
        expected_output=golden.expected_output,
        retrieval_context=documents
    )

    metrics = [
        AnswerRelevancyMetric(
            threshold=0.7,
            model=gemini
        ),
        FaithfulnessMetric(
            threshold=0.7,
            model=gemini
        )
    ]

    assert_test(test_case, metrics)