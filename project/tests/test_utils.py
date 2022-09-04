from typing import Callable


class Tests:
    test_cases: list[Callable] = []
    args: list[tuple[tuple[object, ...], dict[str, object]]] = []

    @classmethod
    def add_test(cls, func: Callable, *args, **kwargs):
        cls.test_cases.append(func)
        cls.args.append((args, kwargs))

    @classmethod
    def run_all(cls):
        passed = 0
        failed = 0

        print("--------------")
        print("Running tests")
        print("--------------")

        for _, (test, args) in enumerate(zip(cls.test_cases, cls.args)):
            print(f"Running test \033[36m{test.__name__}\033[0m: ", end="")

            success = True

            try:
                test(*args[0], **args[1])
            except AssertionError:
                success = False

            if success:
                passed += 1
                print("\033[32mPassed\033[0m")
            else:
                failed += 1
                print("\033[31mFailed\033[0m")

        print("--------------")
        print(f"\033[32mPassed\033[0m {passed} tests")
        print(f"\033[31mFailed\033[0m {failed} tests")
        print("--------------")


def test(func: Callable) -> Callable:
    def inner(*args, **kwargs):
        return args, kwargs

    args, kwargs = inner()
    Tests.add_test(func, *args, **kwargs)

    return lambda: func(*args, **kwargs)


@test
def test_print():
    assert "Hello World" == "Hello World!"


Tests.run_all()
