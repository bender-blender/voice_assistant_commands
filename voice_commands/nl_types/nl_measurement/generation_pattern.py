def create_pattern(optional:bool = False,*args) -> str:
    parts = [arg for arg in args]
    inner = "|".join(parts)
    return f"({inner})? " if optional else f"({inner})"
