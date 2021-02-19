#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def poc(arg):
    '''{
        "name": "poc模板",  # 这里写漏洞名称啥的  
        "desc": "漏洞描述", # 这里写漏洞详细描述+危害
        "grade": "高",      # 等级 
        "keyword": "type:service type:web app:test"}'''  #  这里定义一些关键字，后面可以通过poc.__doc__来查找关键字
    # 可以return 4种类型 ，None和False结果默认不会输出，True会输出 脚本名+参数 ,自定义返回其他类型会输出 脚本名+原始结果
    if arg == '1':
        return None
    elif arg == '2':
        return False
    elif arg == '3':
        return True
    elif arg == '4':
        return arg + ' xxx'

if __name__ == '__main__':
    # 简单单例运行或测试
    import sys
    if len(sys.argv) != 2:
        print("{} IP[:port]".format(sys.argv[0]))
    else:
        print("{} {}".format(sys.argv[1],poc(sys.argv[1])))  
