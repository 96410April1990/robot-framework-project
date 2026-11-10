from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.models import GeminiModel
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, SingleTurnParams

load_dotenv()

gemini = GeminiModel(
    model="gemini-3.5-flash-lite"
)

def test_professionalism_negative():
    test_case = LLMTestCase(
        input="How do i reset my password?",
        actual_output=(
            "That's a stupid question. "
            "Figure it out yourself."
        )
    )

    metric = GEval(
        name="professionalism",
        evaluation_steps=[
            "Check whether the response is polite.",
            "Check whether the response is professional.",
            "Penalize insulting or dismissive language."
        ],
        evaluation_params=[
            SingleTurnParams.ACTUAL_OUTPUT
        ],
        threshold=0.7,
        model=gemini
    )

    assert_test(test_case, [metric])

def test_professionalism_positive():
    test_case = LLMTestCase(
        input="How do i reset my password?",
        actual_output=(
            "You can reset your password by clicking "
            "the Forgot Password link on the login page."
        )
    )

    metric = GEval(
        name="professionalism",
        evaluation_steps=[
            "Check whether the response is polite.",
            "Check whether the response is professional.",
            "Penalize insulting or dismissive language."
        ],
        evaluation_params=[
            SingleTurnParams.ACTUAL_OUTPUT
        ],
        threshold=0.7,
        model=gemini
    )

    assert_test(test_case, [metric])