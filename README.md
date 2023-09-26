# IEEE754repr

IEEE754repr is small Python library which gives you the IEEE-754 representation of a floating point number. IEEE754repr was developed by [Saygın Efe Yıldız](https://github.com/syildizz) and was made with inspiration from the [ieee754](https://github.com/canbula/ieee754) project made by [Bora Canbula](https://github.com/canbula)

When creating the representation you can specify a precision from the list given below or you can even use your own custom precision.
- Half Precision (16 bit: 1 bit for sign + 5 bits for exponent + 10 bits for mantissa)
- Single Precision (32 bit: 1 bit for sign + 8 bits for exponent + 23 bits for mantissa)
- Double Precision (64 bit: 1 bit for sign + 11 bits for exponent + 52 bits for mantissa)
- Quadruple Precision (128 bit: 1 bit for sign + 15 bits for exponent + 112 bits for mantissa)
- Octuple Precision (256 bit: 1 bit for sign + 19 bits for exponent + 236 bits for mantissa)

## Installing

To install IEEE754repr, you have to clone this github repo and put the ieee.py file in the appropriate location.

## Using

After installation, you can import ieee754 and use it in your projects.

### Select a Precision

You can use half, double, quadruple, octuple or custom precision by specifying them in the arguments as thus:
```Python
from ieee754 import IEEE754repr

#for half precision
a = IEEE754repr("5.0123", "HALF")
#for single precision
b = IEEE754repr(0.0013, "FLOAT")
#for quadruple precision
c = IEEE754repr(256, "QUADRUPLE")
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
```Python
#for custom precision
e = ieee754.IEEE754repr("0.0", "CUSTOM", 5, 10)
print(e.get_sign)
#where first integer argument is exponent size,
#second integer argument is mantissa size
```
Note that if the precision argument isn't "CUSTOM", the size values specified get ignored when generating the representation

## Known Issues

- No rounding up is done on the numbers given the precision so the last bit is likely wrong




License
----

MIT License

Copyright (c) 2022 Saygın Efe Yıldız

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
