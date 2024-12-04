from typing import Any, Callable
from selenium.common import exceptions
import time


def calc_time(fun: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator function to calculate the execution time of a function.

    Args:
        fun (function): The function to be decorated.

    Returns:
        function: The decorated function.

    """

    def inner(obj: object, *args: Any, **kwargs: Any) -> object:
        """
        Wrapper function that calculates the execution time of the decorated function.

        Args:
            obj (object): The object instance.
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            object: The result of the decorated function.

        """
        start_time = time.time()
        result = fun(obj, *args, **kwargs)
        end_time = time.time()

        if hasattr(obj, "debug") and getattr(obj, "debug") is True:
            print(f'{"#" * 10} Time take by {fun.__name__}: {end_time - start_time}\n')

        return result

    return inner


def handle_exception(fun: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator function to handle specific exceptions in a function.

    Args:
        fun (function): The function to be decorated.

    Returns:
        function: The decorated function.

    """

    def quit(obj: object) -> None:
        if hasattr(obj, "web_driver"):
            obj.web_driver.quit()

    def inner(obj: object, *args: Any, **kwargs: Any) -> None:
        """
        Wrapper function that handles specific exceptions in the decorated function.

        Args:
            obj (object): The object instance.
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.

        """

        try:
            fun(obj, *args, **kwargs)
        except exceptions.StaleElementReferenceException as e:
            """
            Exception handling for StaleElementReferenceException.

            Args:
                e (exceptions.StaleElementReferenceException): The caught exception.

            """
            print("\nError :: StaleElementReferenceException: ", e.msg)
            quit(obj)
        except KeyboardInterrupt:
            """
            Exception handling for KeyboardInterrupt.

            """
            quit(obj)

    return inner
