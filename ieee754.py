
class IEEE754repr:

   #__length_list = [16, 32, 64, 128, 256]
    __exponent_list = [5, 8, 11, 15, 19]
    __mantissa_list = [10, 23, 52, 112, 236]
    __bias_list = [15, 127, 1023, 16_383, 262_143]

    HALF = 0
    FLOAT = 1
    DOUBLE = 2
    QUADRUPLE = 3
    OCTUPLE = 4
    CUSTOM = -1
    POSITIVE = '0'
    NEGATIVE = '1'
    
    __MANTISSA_MARGIN = 1

    def __init__(self, number: int | float | str, prec: str | int, exp_num: None | int = None, mantissa_num: None | int = None):

        exponent_val, mantissa_val, bias_val = self.__parse_params(prec, exp_num, mantissa_num)
        self.__sign, _number = self.__parse_number(number)
        split_num = self.__num_splitter(self.__sign, _number)
        integer_split_num, (decimal_split_num, rest_zeros) = self.__bin_2_int(split_num[0]), self.__bin_2_dec(split_num[1], mantissa_val)
        bin_num = integer_split_num + decimal_split_num
        if bin_num.count('1') != 0:
            adjusted_bin_num = self.__adjust_binnum(bin_num, mantissa_val, rest_zeros)
            self.__mantissa = adjusted_bin_num[adjusted_bin_num.index('1') + 1 : adjusted_bin_num.index('1') + mantissa_val + 1]
            self.__exponent = self.__exponent_2_bin(integer_split_num, adjusted_bin_num, bias_val, exponent_val)
        else:
            self.__mantissa = '0' * (mantissa_val)
            self.__exponent = '0' * (exponent_val)
        self.__float = self.__sign + self.__exponent + self.__mantissa

    def __str__(self) -> str:
        return self.__float

    def get_binary(self) -> str:
        return self.__float

    # Following piece of code taken from: https://stackoverflow.com/a/2072384
    def get_hex(self) -> str:
        return '%0*X' % ((len(self.__float) + 3) // 4, int(self.__float, 2))

    def get_mantissa(self) -> str:
        return self.__mantissa

    def get_sign(self) -> str:
        return self.__sign

    def get_exponent(self) -> str:
        return self.__exponent

    @classmethod
    def __parse_number(cls, number: int | float | str) -> tuple[str, str]:
        _number = str(number).replace(',', '').replace('_', '').replace(' ', '')
        if '.' not in _number:
            _number += ".0"
        if not _number.replace('.', '').replace('-', '').isdigit() or _number.count('.') != 1:
            raise ValueError('The inputted value "' + str(number) + '" is not a valid number\n'
                             'Valid numbers include:\n'
                             ' "XX",  "XX.XX", \n'
                             '  XX ,   XX.XX , \n'
                             '"-XX", "-XX.XX", \n'
                             ' -XX ,  -XX.XX')

        sign = cls.NEGATIVE if _number[0] == '-' else cls.POSITIVE
        return sign, _number

    @classmethod
    def __parse_params(cls, prec: str | int, exp_num: None | int, mantissa_num: None | int) -> tuple[int, int, int]:
        _prec = str(prec).upper()
        match _prec:
            case c if c in ["HALF", str(cls.HALF)]:
                _prec = cls.HALF
            case c if c in ["FLOAT", str(cls.FLOAT)]:
                _prec = cls.FLOAT
            case c if c in ["DOUBLE", str(cls.DOUBLE)]:
                _prec = cls.DOUBLE
            case c if c in ["QUADRUPLE", str(cls.QUADRUPLE)]:
                _prec = cls.QUADRUPLE
            case c if c in ["OCTUPLE", str(cls.OCTUPLE)]:
                _prec = cls.OCTUPLE
            case c if c in ["CUSTOM", str(cls.CUSTOM)] and str(exp_num).isdigit() and str(mantissa_num).isdigit():
                _prec = cls.CUSTOM
            case _:
                raise ValueError('Not a valid precision argument "' + _prec + '"\n'
                                 'Valid precision arguments:\n'
                                 'HALF: 16 bit, FLOAT: 32 bit, DOUBLE: 64 bit, QUADRUPLE: 128 bit, OCTUPLE: 256 bit, CUSTOM: custom\n'
                                 'Note: CUSTOM must include exponent and mantissa number value in that order\n'
                                 '      Exponent and mantissa argument must only consist of numeric digits')

       #_length_val = self.__length_list[_prec]
        exponent_val = cls.__exponent_list[_prec] if _prec != cls.CUSTOM else int(exp_num)  # type: ignore
        mantissa_val = cls.__mantissa_list[_prec] if _prec != cls.CUSTOM else int(mantissa_num) # type: ignore
        bias_val = cls.__bias_list[_prec] if _prec != cls.CUSTOM else (2 ** (exponent_val - 1)) - 1
        return exponent_val, mantissa_val, bias_val

    @classmethod
    def __bin_2_dec(cls, decimal_split_num: str, mantissa_val: int) -> tuple[str, bool]:

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

        accumulator = ""
        rest_zeros = False
        working = int(decimal_split_num)
        if working == 0:
            rest_zeros = True
            return '0' * (mantissa_val + cls.__MANTISSA_MARGIN), rest_zeros
        threshold = 10**(len(decimal_split_num))
        while (accumulator.count('1') == 0):
            __bin_2_dec_itr()
        shift_amount = len(accumulator)
        for _ in range(mantissa_val + cls.__MANTISSA_MARGIN):
            __bin_2_dec_itr()
            if working == 0:
                accumulator = accumulator + "0" * (mantissa_val + cls.__MANTISSA_MARGIN)
                rest_zeros = True
                break
        return accumulator, rest_zeros

    @staticmethod
    def __bin_2_int(integer_split_num: str) -> str:
        return f'{int(integer_split_num):b}'

    @classmethod
    def __exponent_2_bin(cls, integer_split_num: str, bin_num: str, bias_val: int, exponent_val: int) -> str:
        float_amount = len(integer_split_num) - (bin_num.index('1') + 1)
        float_amount_bin = bin(bias_val + float_amount)[2 : exponent_val + 2]
        while len(float_amount_bin) < exponent_val:
            float_amount_bin = '0' + float_amount_bin
        return float_amount_bin

    @staticmethod
    def __round_up(bin_num: str) -> str:
        _bin_num = list(bin_num)
        if _bin_num[-1] == "0":
            _bin_num[-1] = "1"
        else:
            for i in reversed(range(len(_bin_num))):
                if _bin_num[i] == "0":
                    _bin_num[i] = "1"
                    break
                else:
                    _bin_num[i] = "0"
        return "".join(_bin_num)

    @classmethod
    def __adjust_binnum(cls, bin_num: str, mantissa_val: int, rest_zeros: bool) -> str:
            mantissa_cutoff = bin_num[: bin_num.index('1') + mantissa_val + 1 + cls.__MANTISSA_MARGIN][-2:]

            M, G = mantissa_cutoff            
            if G == "1" and (not rest_zeros or (not rest_zeros and M == "1")):
                _bin_num = cls.__round_up(bin_num[: bin_num.index('1') + mantissa_val + 1])
            else:
                _bin_num = bin_num[: bin_num.index('1') + mantissa_val + 1]
            return _bin_num

    @classmethod
    def __num_splitter(cls, sign: str, number: str) -> list[str]:
        abs_num = number if sign is cls.POSITIVE else number[1:]
        return abs_num.split('.')

