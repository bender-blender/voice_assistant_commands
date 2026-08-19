import pytest
from voice_commands.nl_types.nl_bool.nl_bool import NLBool

@pytest.mark.parametrize('lang, text, expected_value', [
    # English positive
    ("en", "yes", True),
    ("en", "yeah", True),
    ("en", "of course", True),
    # English negative
    ("en", "no", False),
    ("en", "nope", False),
    ("en", "not really", False),

    # Russian positive
    ("ru", "да", True),
    ("ru", "конечно", True),
    ("ru", "ага", True),
    # Russian negative
    ("ru", "нет", False),
    ("ru", "не хочу", False),
    ("ru", "ни за что", False),
    ])
@pytest.mark.asyncio
async def test_nlbool_parse(lang, text, expected_value):
    nl_bool = NLBool(None)
    await nl_bool.did_parse(text)
    assert nl_bool.value == expected_value