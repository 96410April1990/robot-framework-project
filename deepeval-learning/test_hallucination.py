from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.models import GeminiModel
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase

load_dotenv()

gemini = GeminiModel(
    model="gemini-3.5-flash-lite"
)

def test_hallucination_negative():
    test_case = LLMTestCase(
        input="What benefits does the company provide?",
        actual_output=(
            "The company provides health insurance, "
            "dental insurance and free international flights."
        ),
        context=[
            "The company provides health insurance "
            "and dental insurance. "
            "International flights are not provided."
        ]
    )

    metric = HallucinationMetric(
        threshold=0.7,
        model=gemini,
        include_reason=True
    )

    assert_test(test_case, [metric])

def test_hallucination_positive():
    test_case = LLMTestCase(
        input="What benefits does the company provide?",
        actual_output=(
            "The company provides health insurance "
            "and dental insurance"
        ),
        context=[
            "The company provides health insurance "
            "and dental insurance. "
            "International flights are not provided."
        ]
    )

    metric = HallucinationMetric(
        threshold=0.7,
        model=gemini,
        include_reason=True
    )

    assert_test(test_case, [metric])