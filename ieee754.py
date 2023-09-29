
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

    def __init__(self, number, prec: str, exp_num = None, mantissa_num = None):

        _exponent_val, _mantissa_val, _bias_val = self.__parse_params(prec, exp_num, mantissa_num)
        _number = self.__is_valid_num(number)
        self.__sign = self.NEGATIVE if _number[0] == '-' else self.POSITIVE
        _split_num = self.__num_splitter(self.__sign, _number)
        _bin_num = self.__bin_2_int(_split_num) + self.__bin_2_dec(_split_num, _mantissa_val)
        if _bin_num.count('1') != 0:
            self.__mantissa = _bin_num[_bin_num.index('1') + 1 : _bin_num.index('1') + _mantissa_val + 1]
            self.__exponent = self.__exponent_2_bin(_split_num, _bin_num, _bias_val, _exponent_val)
        else:
            self.__mantissa = '0' * (_mantissa_val)
            self.__exponent = '0' * (_exponent_val)
        self.__float = self.__sign + self.__exponent + self.__mantissa

    def __str__(self):
        return self.__float

    def get_binary(self):
        return self.__float

    # Following piece of code taken from: https://stackoverflow.com/a/2072384
    def get_hex(self):
        return '%0*X' % ((len(self.__float) + 3) // 4, int(self.__float, 2))

    def get_mantissa(self):
        return self.__mantissa

    def get_sign(self):
        return self.__sign

    def get_exponent(self):
        return self.__exponent

    @staticmethod
    def __is_valid_num(number):
        number = str(number).replace(',', '').replace('_', '').replace(' ', '')
        if '.' not in number:
            number += ".0"
        if not number.replace('.', '').replace('-', '').isdigit() or number.count('.') != 1:
            raise ValueError("The inputted value was not a valid number\n"
                             "Valid numbers include:\n"
                             "\"XX\", \"XX.XX\", XX, XX.XX")
        return number

    @classmethod
    def __parse_params(cls, prec, exp_num, mantissa_num):
        _prec = str(prec)
        _prec.upper()
        match _prec:
            case "HALF":
                _prec = cls.HALF
            case "FLOAT":
                _prec = cls.FLOAT
            case "DOUBLE":
                _prec = cls.DOUBLE
            case "QUADRUPLE":
                _prec = cls.QUADRUPLE
            case "OCTUPLE":
                _prec = cls.OCTUPLE
            case "CUSTOM" if str(exp_num).isdigit() and str(mantissa_num).isdigit():
                _prec = cls.CUSTOM
            case _:
                raise ValueError("Not a valid precision argument\n"
                                 "Valid precision arguments:\n"
                                 "HALF: 16 bit, FLOAT: 32 bit, DOUBLE: 64 bit, QUADRUPLE: 128 bit, OCTUPLE: 256 bit, CUSTOM: custom\n"
                                 "Note: CUSTOM must include exponent and mantissa number value in that order")
       
       #_length_val = self.__length_list[_prec]
        _exponent_val = cls.__exponent_list[_prec] if _prec != cls.CUSTOM else int(exp_num)
        _mantissa_val = cls.__mantissa_list[_prec] if _prec != cls.CUSTOM else int(mantissa_num)
        _bias_val = cls.__bias_list[_prec] if _prec != cls.CUSTOM else (2 ** (_exponent_val - 1)) - 1
        return _exponent_val, _mantissa_val, _bias_val

    @staticmethod
    def __bin_2_dec(_split_num, _mantissa_val):
        def __bin_2_dec_itr():
            nonlocal tempstr
            nonlocal temp
            nonlocal temp2
            temp *= 2
            if temp >= temp2:
                tempstr += '1'
                temp -= temp2
            else:
                tempstr += '0'
            return tempstr
        tempstr = ""
        temp = int(_split_num[1])
        if temp != 0:
            temp2 = 10**(len(_split_num[1]))
        else:
            return '0' * (_mantissa_val)
        i = 0
        while (tempstr.count('1') == 0):
            __bin_2_dec_itr()
            i += 1
        for _ in range(0,_mantissa_val + i):
            __bin_2_dec_itr()
        return tempstr

    @staticmethod
    def __bin_2_int(_split_num):
        return bin(int(_split_num[0]))[2:]

    @classmethod
    def __exponent_2_bin(cls, _split_num, _bin_num, _bias_val, _exponent_val):
        float_amount = len(cls.__bin_2_int(_split_num)) - (_bin_num.index('1') + 1)
        float_amount_bin = bin(_bias_val + float_amount)[2 : _exponent_val + 2]
        while len(float_amount_bin) < _exponent_val:
            float_amount_bin = '0' + float_amount_bin
        return float_amount_bin

    @classmethod
    def __num_splitter(cls, _sign, _number):
        abs_num = _number if _sign is cls.POSITIVE else _number[1:]
        return abs_num.split('.')
