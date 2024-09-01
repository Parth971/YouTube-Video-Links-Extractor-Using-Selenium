from selenium.common import exceptions
import time


def calc_time(fun):
    """
    Decorator function to calculate the execution time of a function.

    Args:
        fun (function): The function to be decorated.

    Returns:
        function: The decorated function.

    """

    def inner(*args, **kwargs):
        """
        Wrapper function that calculates the execution time of the decorated function.

        Args:
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            object: The result of the decorated function.

        """
        start_time = time.time()
        result = fun(*args, **kwargs)
        end_time = time.time()

        if hasattr(args[0], "debug") and getattr(args[0], "debug"):
            print(f'{"#" * 10} Time take by {fun.__name__}: {end_time - start_time}\n')

        return result

    return inner


def handle_exception(fun):
    """
    Decorator function to handle specific exceptions in a function.

    Args:
        fun (function): The function to be decorated.

    Returns:
        function: The decorated function.

    """

    def inner(*args, **kwargs):
        """
        Wrapper function that handles specific exceptions in the decorated function.

        Args:
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.

        """

        try:
            return fun(*args, **kwargs)
        except exceptions.StaleElementReferenceException as e:
            """
            Exception handling for StaleElementReferenceException.

            Args:
                e (exceptions.StaleElementReferenceException): The caught exception.

            """
            print("\nError :: StaleElementReferenceException: ", e.msg)
        except KeyboardInterrupt:
            """
            Exception handling for KeyboardInterrupt.

            """
            pass

        args[0].quit()

    return inner
