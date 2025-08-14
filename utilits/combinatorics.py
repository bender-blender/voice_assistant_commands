import asyncio

# from functools import wraps
import time
from typing import Any, Awaitable, Callable

# General optimizations:
# - caching


async def async_combinatorics[
    T: Any
](
    phrase: str,
    parser: Callable[[str], Awaitable[T | None]],
    desc_filter: bool = True,
    min_delay_sec: float = 0,
) -> (
    tuple[str, T] | None
):
    """For clean and dirty providers, but works better with clean"""

    words = phrase.replace("-", " ").split(" ")
    count_words = len(words)
    substring = []
    for i in range(count_words):
        for j in range(i + 1, count_words + 1):
            substring.append(words[i:j])

    substring_dictionary: dict[T, str] = {}

    last_sent_request = time.monotonic()

    async def task(sub):
        nonlocal last_sent_request

        while time.monotonic() - last_sent_request < min_delay_sec:
            await asyncio.sleep(0.01)

        last_sent_request = time.monotonic()
        result = await parser(" ".join(sub))

        if result is not None:
            if result in substring_dictionary:
                if desc_filter:
                    if len(substring_dictionary[result]) > len(" ".join(sub)):
                        substring_dictionary[result] = " ".join(sub)
                else:
                    if len(substring_dictionary[result]) < len(" ".join(sub)):
                        substring_dictionary[result] = " ".join(sub)
            else:
                substring_dictionary[result] = " ".join(sub)

    tasks = [task(sub) for sub in substring]
    await asyncio.gather(*tasks)

    sorted_dict = sorted(substring_dictionary.items(), key=lambda item: len(item[1]), reverse=True)

    if not sorted_dict:
        return None

    value = sorted_dict[0][0]
    return_the_word = sorted_dict[0][1]
    return return_the_word, value
