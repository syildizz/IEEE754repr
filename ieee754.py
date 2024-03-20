
class IEEE754repr:

    # The precision lists that hold the sizes of the sections for different floating point precisions.
    # __length_list = [16, 32, 64, 128, 256]
    __exponent_list = [5, 8, 11, 15, 19]
    __mantissa_list = [10, 23, 52, 112, 236]
    __bias_list = [15, 127, 1023, 16_383, 262_143]

    # The precision indices used for indexing the precision lists as enums to specify precisions.
    HALF = 0
    FLOAT = 1
    DOUBLE = 2
    QUADRUPLE = 3
    OCTUPLE = 4
    CUSTOM = -1
    # The sign bit used as enums.
    POSITIVE = '0'
    NEGATIVE = '1'
    
    # Margin value used internally as padding after the mantissa length.
    __MANTISSA_MARGIN = 1

    def __init__(self, number: int | float | str, prec: str | int, exp_num: None | int = None, mantissa_num: None | int = None):

        # Parse the parameters passed to the constructor and return the number of bits that each section of the floating point number is going to consist of.
        # Raises ValueError in case of incorrect params.
        exponent_val, mantissa_val, bias_val = self.__parse_params(prec, exp_num, mantissa_num)

        # Parse the number passed to the constructor and return the number and the sign bit of the binary representation of the number.
        # Raises ValueError in case of incorrect params.
        self.__sign, _number = self.__parse_number(number)

        # Split the number from the dot into the integer and the decimal section and return as tuple.
        split_num = _number.split(".")

        # Turn both of the halves into their binary representations and return the result. Also return rest_zeros for rounding.
        integer_split_num, (decimal_split_num, rest_zeros) = self.__bin_2_int(split_num[0]), self.__bin_2_dec(split_num[1], mantissa_val)

        # Add together the binary representations together to get an unfinished mantissa section
        bin_num = integer_split_num + decimal_split_num

        # Check if the number is not 0.
        if bin_num.count('1') != 0:
            # Adjust bin_num by resizing and rounding if necessary.
            adjusted_bin_num = self.__adjust_binnum(bin_num, mantissa_val, rest_zeros)

            # Adjust the mantissa section into right amount of bits.
            self.__mantissa = self.__mantissa_2_bin(adjusted_bin_num, mantissa_val)

            # Calculate and return the exponent bits.
            self.__exponent = self.__exponent_2_bin(integer_split_num, adjusted_bin_num, bias_val, exponent_val)

        # In case zero, just set the mantissa and exponent bits to the right amount of zeros.
        else:
            self.__mantissa = '0' * (mantissa_val)
            self.__exponent = '0' * (exponent_val)

        # Combine the bits and get the binary representation of the floating point number.
        self.__float = self.__sign + self.__exponent + self.__mantissa

    def __str__(self) -> str:
        """Return the binary representation of the floating point number as string."""
        return self.__float

    def get_binary(self) -> str:
        """Return the binary representation of the floating point number as string."""
        return self.__float

    # Following piece of code taken from: https://stackoverflow.com/a/2072384
    def get_hex(self) -> str:
        """Return the hexadecimal representation of the floating point number as string."""
        return '%0*X' % ((len(self.__float) + 3) // 4, int(self.__float, 2))

    def get_mantissa(self) -> str:
        """Return the mantissa portion of the binary representation of the floating point number as string."""
        return self.__mantissa

    def get_sign(self) -> str:
        """Return the sign portion of the binary representation of the floating point number as string."""
        return self.__sign

    def get_exponent(self) -> str:
        """Return the exponent portion of the binary representation of the floating point number as string."""
        return self.__exponent

    @classmethod
    def __parse_number(cls, number: int | float | str) -> tuple[str, str]:
        """
        Parse the number into a standart format and return the parsed number and the sign bit.

        e.g. "-1_234.5678" -> "0" (cls.NEGATIVE), 
                              "1234.5678"

        :param number: The number that is going to be parsed.
        :returns: Tuple (sign, number) containing:
            - sign: The sign bit of the binary representation of the number.
            - number: The parsed number.
        :raises ValueError: Raises ValueError in case of incorrect number argument.
        """
        # Ignore insignificant and whitespace characters.
        _number = str(number).replace(',', '').replace('_', '').replace(' ', '')

        # Add the decimal zero if the number is integer.
        if '.' not in _number:
            _number += ".0"
        
        # If the inputted number format is incorrect raise ValueError.
        if not _number.replace('.', '').replace('-', '').isdigit() or _number.count('.') != 1:
            raise ValueError('The inputted value "' + str(number) + '" is not a valid number\n'
                             'Valid number formats include:\n'
                             ' "XX",  "XX.XX", \n'
                             '  XX ,   XX.XX , \n'
                             '"-XX", "-XX.XX", \n'
                             ' -XX ,  -XX.XX')

        # Determine the sign bit.
        sign = cls.NEGATIVE if _number[0] == '-' else cls.POSITIVE

        # Return the sign bit and parsed number.
        return sign, _number

    @classmethod
    def __parse_params(cls, prec: str | int, exp_num: None | int, mantissa_num: None | int) -> tuple[int, int, int]:
        """
        Calculate the number of bits of the floating point sections and the bias value.

        e.g. "FLOAT" -> 8      (exponent_val), 
                        23     (mantissa_val), 
                        1023    (bias_val)

        :param prec: The supplied precision value.
        :param exp_num: The number of bits that the exponent section should be if prec is specified as custom.
        :param mantissa_num: The number of bits that the mantissa section should be if prec is specified as custom.
        :returns: Tuple (exponent_val, mantissa_val, bias_val) containing:
            - exponent_val: Number of bits that are going to be used for the exponent section.
            - mantissa_val: Number of bits that are going to be used for the mantissa section.
            - bias_val: The bias value for the specified precision.
        :raises ValueError: Raises ValueError in case of incorrect params.
        """

        # Ignore precision argument capitalization.
        _prec = str(prec).upper()

        # Parse the precision parameter and determine the precision accordingly.
        if _prec in ["HALF", str(cls.HALF)]:
            _prec = cls.HALF
        elif _prec in ["FLOAT", str(cls.FLOAT)]:
            _prec = cls.FLOAT
        elif _prec in ["DOUBLE", str(cls.DOUBLE)]:
            _prec = cls.DOUBLE
        elif _prec in ["QUADRUPLE", str(cls.QUADRUPLE)]:
            _prec = cls.QUADRUPLE
        elif _prec in ["OCTUPLE", str(cls.OCTUPLE)]:
            _prec = cls.OCTUPLE
        elif _prec in ["CUSTOM", str(cls.CUSTOM)] and str(exp_num).isdigit() and str(mantissa_num).isdigit():
            _prec = cls.CUSTOM
        else:
            raise ValueError('Not a valid precision argument "' + _prec + '"\n'
                             'Valid precision arguments:\n'
                             'HALF: 16 bit, FLOAT: 32 bit, DOUBLE: 64 bit, QUADRUPLE: 128 bit, OCTUPLE: 256 bit, CUSTOM: custom\n'
                             'Note: CUSTOM must include exponent and mantissa number value in that order\n'
                             '      Exponent and mantissa argument must only consist of numeric digits')

        # Determine the number of bits used for each section of the binary representation based on precision and parameters and calculate the bias value.
       #length_val = self.__length_list[_prec]
        exponent_val = cls.__exponent_list[_prec] if _prec != cls.CUSTOM else int(exp_num)  #  type: ignore
        mantissa_val = cls.__mantissa_list[_prec] if _prec != cls.CUSTOM else int(mantissa_num) #  type: ignore
        bias_val = cls.__bias_list[_prec] if _prec != cls.CUSTOM else (2 ** (exponent_val - 1)) - 1

        # Return the numbers of bits which are going to be used for the exponent and mantissa sections and return the bias value.
        return exponent_val, mantissa_val, bias_val

    @classmethod
    def __bin_2_dec(cls, decimal_split_num: str, mantissa_val: int) -> tuple[str, bool]:
        """
        Take the decimal value (after the dot e.g. 0.1234) and turn it into a binary representation.

        e.g. 1234.5678 -> 5678 -> 100100101011011010101110 (for float mantissa val), 
                                  False                     (there exists a one after the cutoff point)

        :param decimal_split_num: The decimal value.
        :param mantissa_val: The number of bits that the mantissa section is going to consist of.
        :returns: Tuple (decimal_repr, rest_zeros) containing
            - decimal_repr: The binary representation of the decimal value
            - rest_zeros: Information about whether after the cutoff point of decimal_repr there exists only zeros.
        """
        # The decimal number is represented as an integer for the calculation.
        #    e.g. working:   0.5678 ->  5678
        #         threshold: 0.5678 -> 10000
        # Instead of multiplying the floating point value by two, we process the number as integers as to
        # not use floating point numbers in our calculations.

        # Internal function used for calculating the next binary digit of the number.
        def __bin_2_dec_itr():
            nonlocal accumulator
            nonlocal working
            nonlocal threshold
            working *= 2
            if working >= threshold:
                accumulator += '1'
                working -= threshold
            else:
                accumulator += '0'

        # Accumulator is the decimal representation that is going to be returned from this function.
        accumulator = ""
        # Rest zeroes is set to true so that if there is any remainder in the working then we know that
        # after the cutoff point there will be a zero eventually.
        rest_zeros = False
        working = int(decimal_split_num)

        # Return zero if the number is zero.
        if working == 0:
            rest_zeros = True
            return '0' * (mantissa_val + cls.__MANTISSA_MARGIN), rest_zeros

        # Where the calculation takes place.
        threshold = 10**(len(decimal_split_num))
        ## Generate binary digits until we hit a one.
        while (accumulator.count('1') == 0):
            __bin_2_dec_itr()

        ## Generate binary digits until we have generated at least enough numbers for the mantissa section
        for _ in range(mantissa_val + cls.__MANTISSA_MARGIN):
            __bin_2_dec_itr()
            # If the remainder is zero, generate at least enough numbers for the mantissa section
            if working == 0:
                accumulator = accumulator + "0" * (mantissa_val + cls.__MANTISSA_MARGIN)
                rest_zeros = True
                break
        return accumulator, rest_zeros

    @staticmethod
    def __bin_2_int(integer_split_num: str) -> str:
        """
        Take the integer value and turn it into a binary representation.

        e.g. 1234.5678 -> 1234 -> 10011010010

        :param integer_split_num: The integer value.
        :returns: The binary representation of the integer value.
        """
        # Uses Python's interal f-string to do the conversion.
        return f'{int(integer_split_num):b}'

    @classmethod
    def __exponent_2_bin(cls, integer_split_num: str, bin_num: str, bias_val: int, exponent_val: int) -> str:
        """
        Calculates and returns the bits for the exponent section of the floating point representation.

        :param integer_split_num: The binary representation of the integer value.
        :param bin_num: The binary representation of the number.
        :param bias_val: The bias value of the floating point number.
        :param exponent_val: The number of bits that are going to be used for the exponent section
        :returns: The binary representation of the exponent section.
        """
        # If exponent section's size is specified as zero, do not generate an exponent section.
        if exponent_val == 0:
            return ""
        # float_amount represents how much offset there is from the binary number to the first one bit.
        float_amount = len(integer_split_num) - (bin_num.index('1') + 1)
        # float_amount_bin is the calculated binary representation for the exponent section.
        float_amount_bin = bin(bias_val + float_amount)[2 : exponent_val + 2]

        # Pad out the the float_amount_bin with zeros until the right size is reacted.
        while len(float_amount_bin) < exponent_val:
            float_amount_bin = '0' + float_amount_bin

        return float_amount_bin

    @staticmethod
    def __mantissa_2_bin(bin_num: str, mantissa_val: int) -> str:
        """
        Calculates and returns the bits for the mantissa section of the floating point representation.

        :param bin_num: The binary representation of the number.
        :param mantissa_val: The number of bits that are going to be used for the mantissa section.
        :returns: The binary representation of the mantissa section.
        """
        # If exponent section's size is specified as zero, do not generate an exponent section.
        if mantissa_val == 0:
            return ""

        # Resize the mantissa section to the correct size.
        return bin_num[bin_num.index('1') + 1 : bin_num.index('1') + mantissa_val + 1]

    @staticmethod
    def __round_up(bin_num: str) -> str:
        """
        Rounds up the binary number by adding one to it in binary.

        e.g. 10011010010 -> 10011010011

        :param bin_num: The binary number.
        :returns: The rounded up binary number.
        """
        # Turn the bin_num to a list for mutability.
        _bin_num = list(bin_num)

        # If the LSB is zero, then turn it into one and return.
        if _bin_num[-1] == "0":
            _bin_num[-1] = "1"
        else:
            # Search for a zero from the start and flip the bits until a zero is found.
            for i in reversed(range(len(_bin_num))):
                if _bin_num[i] == "0":
                    _bin_num[i] = "1"
                    break
                else:
                    _bin_num[i] = "0"
        
        # Return bin_num to a string and return.
        return "".join(_bin_num)

    @classmethod
    def __adjust_binnum(cls, bin_num: str, mantissa_val: int, rest_zeros: bool) -> str:
        """
        Adjust the binary number by resizing it to the correct size and rounding it up if necessary.

        :param bin_num: The binary number.
        :param mantissa_val: The number of bits that are going to be used for the mantissa section.
        :rest_zeros: Information about whether there exists only zeros after the cutoff point of the bin_num.
        :returns: The adjusted binary number resized and rounded.
        """
        # Cut out the relevant section from the mantissa.
        mantissa_cutoff = bin_num[: bin_num.index('1') + mantissa_val + 1 + cls.__MANTISSA_MARGIN][-2:]

        # The rounding is done using the "round to nearest, ties to even algorithm." 
        # The calculations for the rounding consist of three variables which represent the following sections:
        #     XXXXM.G(rest_zeros)
        # Where:
        #     X is any bit.
        #     M is the LSB.
        #     G is the bit after the LSB.
        #     rest_zeros is the information about whether any of the bits after G have zeroes in them.
        # Rounding is done if:
        #     G is 1 and
        #         if G is zero then the decimal section is <0.5 and shouldn't be rounded.
        #         rest_zeros is false or
        #             if rest_zeros is false then the number ends with 0.500...01 and therefore should be rounded.
        #         rest_zeros is true and M is 1
        #             if rest_zeros is true then the number ends with 0.5 and should be rounded if LSB is 1 (number is odd).
        M, G = mantissa_cutoff            
        if G == "1" and (not rest_zeros or (rest_zeros and M == "1")):
            _bin_num = cls.__round_up(bin_num[: bin_num.index('1') + mantissa_val + 1])
        else:
            _bin_num = bin_num[: bin_num.index('1') + mantissa_val + 1]
        return _bin_num
