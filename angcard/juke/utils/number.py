# encoding=utf-8
import re

class Number:
    @staticmethod
    def is_decimal(number):
        ''' 判断一个数是否是小数 '''
        pattern = re.compile(r'^(0|[1-9]\d*)\.(\d{1,2})$')
        match = pattern.match(number)
        return True if match else False
