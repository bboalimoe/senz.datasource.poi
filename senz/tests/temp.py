__author__ = 'wuzhifan'

import json

if __name__ == '__main__':
    a = [u'\u516c\u76ca', u'\u8bb2\u5ea7', u'\u65c5\u884c', u'\u5176\u4ed6', u'\u805a\u4f1a', u'\u8fd0\u52a8', u'\u97f3\u4e50', u'\u7535\u5f71', u'\u620f\u5267', u'\u5c55\u89c8']
    print json.dumps(a, encoding='UTF-8', ensure_ascii=False)
