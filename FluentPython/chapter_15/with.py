
import sys
from contextlib import contextmanager


class LookingGlass:

    def __enter__(self):
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'JACK'

    def reverse_write(self, text):
        return self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print("Please DO NOT divide by zero!")
            return True


@contextmanager
def looking_glass():
    original_write = sys.stdout.write

    # def reverse_write(text):
    #     return original_write(text[::-1])

    # sys.stdout.write = reverse_write
    sys.stdout.write = lambda text: original_write(text[::-1])
    yield 'HUGO'
    sys.stdout.write = original_write

if __name__ == "__main__":
    with LookingGlass() as what:
        print("A, B, C")
        print(what)
    print(what)
    print('A, B, C')

    print("***********contextmanager example as follow************")

    with looking_glass() as what:
        print("ABC")
        print(what)
    print(what)
    print("ABC")
