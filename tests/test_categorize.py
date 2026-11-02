from categorize import rule_category, DEBIT_RULES, CREDIT_RULES,model_category,debit_prompt
from unittest.mock import patch

def test_debit_rule_category():
    result = rule_category("Paid to Swiggy", DEBIT_RULES)
    assert result == "Food & Dining"


def test_credit_rule_category():
    result = rule_category("Cashback received", CREDIT_RULES)
    assert result == "Cashback & Rewards"


def test_unknown_transaction():
    result = rule_category("XYZ transaction", DEBIT_RULES)
    assert result is None

from unittest.mock import patch

@patch("categorize.ollama.chat")
def test_model_category(mock_chat):
    mock_chat.return_value = {
        "message": {
            "content": "Food & Dining"
        }
    }

    result = model_category("Paid to unknown restaurant", debit_prompt)

    assert result == "Food & Dining"
    mock_chat.assert_called_once()