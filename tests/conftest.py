_last_group = None


def pytest_runtest_setup(item):
    global _last_group

    test_name = item.originalname or item.name

    if test_name != _last_group:
        print("\n" + "=" * 80)
        print(f"Running: {test_name}")
        print("=" * 80)
        _last_group = test_name