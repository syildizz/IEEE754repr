# IEEE754repr

IEEE754repr is small python library which gives you the IEEE-754 representation of a floating point number. IEEE754repr was developed by [Saygın Efe Yıldız](https://github.com/syildizz) and was made with inspiration from the [ieee754](https://github.com/canbula/ieee754) project made by [Bora Canbula](https://github.com/canbula).

When creating the representation you can specify a precision from the list given below or you can even use your own custom precision.
- Half Precision (16 bit: 1 bit for sign + 5 bits for exponent + 10 bits for mantissa)
- Single Precision (32 bit: 1 bit for sign + 8 bits for exponent + 23 bits for mantissa)
- Double Precision (64 bit: 1 bit for sign + 11 bits for exponent + 52 bits for mantissa)
- Quadruple Precision (128 bit: 1 bit for sign + 15 bits for exponent + 112 bits for mantissa)
- Octuple Precision (256 bit: 1 bit for sign + 19 bits for exponent + 236 bits for mantissa)

## Installing

### Dowload the repository

This can be done either using git by running

```bash
git clone https://github.com/syildizz/IEEE754repr.git
```

or you can [download the zip archive of this repository](https://github.com/syildizz/IEEE754repr/archive/refs/heads/main.zip).

### Install using pip locally

You can install locally using pip by running

```bash
python3 -m pip install .
```

The package will be installed to your Python environment with the name "ieee754repr"

## Usage

The package structure consists of

- ieee754repr (The main package)
    - ieee754 (The package here the main python code resides)
        - IEEE754repr (The class that does the binary representation)
    - pfloat (The c extension package for testing purposes)
        - pfloat (The function that calculates the binary representation empirically)

You can import the IEEE754repr class from the ieee754 module like so

```python
from ieee754repr.ieee754 import IEEE754repr
```

You can import the pfloat function from the pfloat module like so

```python
from ieee754repr.pfloat import pfloat
```

The pfloat package is used for testing purposes but it is faster than the ieee754 package if you want to calculate single or double precision. 
For custom precision you cannot use pfloat. 

### Select a Precision

You can use half, double, single, quadruple, octuple or custom precision by specifying them in the constructors arguments as strings or by using their internal representation in the IEEE754repr class as thus:
```python
from ieee754repr.ieee754 import IEEE754repr

#for half precision
a = IEEE754repr("5.0123", "HALF")
#for single precision
b = IEEE754repr(0.0013, IEEE754repr.FLOAT)
#for quadruple precision
c = IEEE754repr(256, IEEE754repr.QUADRUPLE)
#for octuple precision
d = IEEE754repr("234_546", "OCTUPLE")
print(a)
print(a.get_mantissa())
print(b.get_binary())
print(c.get_hex())
print(d.get_exponent())
```

### Using a Custom Precision

You can define the size of the exponent and the mantissa in the third and fourth arguments respectively.
```python
#for custom precision
e = ieee754repr.ieee754.IEEE754repr("0.0", "CUSTOM", 5, 10)
print(e.get_sign())
#where first integer argument is exponent size,
#second integer argument is mantissa size
```
Note that if the precision argument isn't "CUSTOM", the size values specified get ignored when generating the representation.

## Testing

This package can be tested after the installation by running

```bash
python3 test/test.py
```

If you want to change the range of values that get tested, you can edit the digit_count variable to your liking.

## Rounding

Rounding is used when generating the floating point numbers.
Rounding is calculated using a "round to nearest, ties to even" algorithm.

License
----

### MIT License

Copyright (c) 2024 Saygın Efe Yıldız

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
