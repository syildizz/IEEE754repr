from ieee754repr.ieee754 import IEEE754repr
from ieee754repr.pfloat import pfloat #type: ignore
from typing import Iterator

def compare_analytical_empirical(val: str, prec: str) -> None:
    """Compare the generated value from the IEEE754repr class and the empirical value generated from pfloat function."""
    prediction: str = str(IEEE754repr(val, prec))
    real: str = pfloat(val, prec)
    assert real == prediction, f"\nExpected   {real} is not equal to \n" \
                                f"Prediction {prediction}"
    print("✓ \r", end="")

def generate_floating_range(integer_digit_num: int, decimal_digit_num: int) -> Iterator[float]:
    """
    Generate numbers that have integer_digit_num number of digits before dot, decimal_digit_num number of digits after dot.

    e.g. XX.XXX -> (2,3) -> From range -10^2 (-99) to 10^2 (99) with decimal resolution of 3 digits (0.001).
    """
    total_digit_num: int = integer_digit_num + decimal_digit_num
    for i in range(-10**total_digit_num, 10**total_digit_num):
        yield i/10**decimal_digit_num

# Change this variables to change the floating range
# e.g. XX.XXXX -> (2,4) -> From -99.9999 to 99.9999
digit_count: tuple[int, int] = (2,4)

print("Empirical Test")
for fval in generate_floating_range(*digit_count):
    print(f"Single: {fval:.4f} ", end=" ")
    compare_analytical_empirical(str(fval), "FLOAT")

print()
for dval in generate_floating_range(*digit_count):
    print(f"Double: {dval:.4f} ", end=" ")
    compare_analytical_empirical(str(dval), "DOUBLE")

print()
