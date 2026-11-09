from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.models import GeminiModel
from deepeval.metrics import ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase, ToolCall

load_dotenv()

gemini = GeminiModel(
    model="gemini-3.5-flash-lite"
)

def test_correct_tool_selection():
    test_case = LLMTestCase(
        input="What is the leave policy?",
        actual_output="Employees receive 20 annual leave days.",
        tools_called=[
            ToolCall(name="SearchHRPolicy")
        ],
        expected_tools=[
            ToolCall(name="SearchHRPolicy")
        ]
    )

    metrics = ToolCorrectnessMetric(
        threshold=1.0,
        model=gemini
    )

    assert_test(test_case, [metrics])