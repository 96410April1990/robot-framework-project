from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.models import GeminiModel
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

load_dotenv()

gemini = GeminiModel(
    model="gemini-3.5-flash-lite"
)

def test_answer_relavancy():
    test_case = LLMTestCase(
        input="What is Selenium?",
        actual_output=(
            "Selenium is an open-source framework "
            "for automating web browsers."
        )
    )

    metric = AnswerRelevancyMetric(
        threshold=0.7,
        model=gemini,
        include_reason=True
    )

    assert_test(test_case, [metric])
