"""Helping package with pre-setup debug function.

Use by placing following line anywhere you'd need to start debugger.

    import mapz.tests.debug
"""

import debugpy  # pragma: no cover


def debug():  # pragma: no cover
    """Start debugpy debugger."""

    debugpy.listen(("0.0.0.0", 10001))
    print(
        "⏳ VS Code debugger can now be attached, press F5 in VS Code ⏳",
        flush=True,
    )
    debugpy.wait_for_client()
    print("🎉 VS Code debugger attached, enjoy debugging 🎉", flush=True)


debug()
