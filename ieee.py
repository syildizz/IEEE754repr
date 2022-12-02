
class IEEErepr:

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

    class UndefinedArgumentException(Exception):
        pass

    class NotAValidNumberException(Exception):
        pass

    def __init__ (self, number, prec: str, exp_num = None, mantissa_num = None):

        try:
            self.__prec = self.__is_valid_prec(prec, exp_num, mantissa_num)
        
        except IEEErepr.UndefinedArgumentException:
            print("UndefinedArgumentException: Not a valid precision argument")
            print("Valid precision arguments:")
            print("HALF: 16 bit, FLOAT: 32 bit, DOUBLE: 64 bit, QUADRUPLE: 128 bit, OCTUPLE: 256 bit, CUSTOM: custom")
            print("Note: CUSTOM must include exponent and mantissa number value in that order")
            exit()
        
        #self.__length_val = IEEErepr.__length_list[self.__prec]
        try:
            self.__number = self.__is_valid_num(number)

        except IEEErepr.NotAValidNumberException:
            print("NotAValidNumberException: The inputted value was not a valid number")
            print("Valid numbers include:")
            print("\"XX\", \"XX.XX\", XX, XX.XX")
            exit()

        self.__exponent_val = IEEErepr.__exponent_list[self.__prec] if self.__prec != IEEErepr.CUSTOM else int(exp_num)  # type: ignore
        self.__mantissa_val = IEEErepr.__mantissa_list[self.__prec] if self.__prec != IEEErepr.CUSTOM else int(mantissa_num)  # type: ignore
        self.__bias_val = IEEErepr.__bias_list[self.__prec] if self.__prec != IEEErepr.CUSTOM else (2 ** (self.__exponent_val - 1)) - 1
        self.__sign = IEEErepr.NEGATIVE if self.__number[0] == '-' else IEEErepr.POSITIVE
        self.__split_num = self.__num_splitter()
        self.__bin_num = self.__bin_2_int() + self.__bin_2_dec()
        if self.__bin_num.count('1') != 0:
            self.__mantissa = self.__bin_num[self.__bin_num.index('1') + 1:self.__bin_num.index('1') + self.__mantissa_val + 1]
            self.__exponent = self.__exponent_2_bin()
        else:
            self.__mantissa = '0' * (self.__mantissa_val)
            self.__exponent = '0' * (self.__exponent_val)
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

    def __is_valid_num(self, number):
        number = str(number).replace(',', '').replace('_', '').replace(' ', '')
        if '.' not in number:
            number += ".0"
        if not number.replace('.', '').replace('-', '').isdigit() or number.count('.') != 1:
                raise IEEErepr.NotAValidNumberException
        return number

    def __is_valid_prec(self, prec, e_num, m_num):
        prec = str(prec)
        prec.upper()
        match prec:
            case "HALF":
                return IEEErepr.HALF
            case "FLOAT":
                return IEEErepr.FLOAT
            case "DOUBLE":
                return IEEErepr.DOUBLE
            case "QUADRUPLE":
                return IEEErepr.QUADRUPLE
            case "OCTUPLE":
                return IEEErepr.OCTUPLE
            case "CUSTOM" if str(e_num).isdigit() and str(m_num).isdigit():
                return IEEErepr.CUSTOM
            case _:
                raise IEEErepr.UndefinedArgumentException

    def __bin_2_dec(self):
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
        temp = int(self.__split_num[1])
        if temp != 0:
            temp2 = 10**(len(self.__split_num[1]))
        else:
            return '0' * (self.__mantissa_val) #replaced + 1 with * 2 
        i = 0
        while (tempstr.count('1') == 0):
            __bin_2_dec_itr()
            i += 1
        for _ in range(0,self.__mantissa_val + i):
            __bin_2_dec_itr()
        return tempstr
    
    def __bin_2_int(self):
        return bin(int(self.__split_num[0]))[2:]

    def __exponent_2_bin(self):
        float_amount = len(self.__bin_2_int()) - (self.__bin_num.index('1') + 1) 
        float_amount_bin = bin(self.__bias_val + float_amount)[2:self.__exponent_val + 2]
        while len(float_amount_bin) < self.__exponent_val:
            float_amount_bin = '0' + float_amount_bin
        return float_amount_bin
    
    def __num_splitter(self):
        self.__abs_num = self.__number if self.__sign is IEEErepr.POSITIVE else self.__number[1:]
        return self.__abs_num.split('.')
    