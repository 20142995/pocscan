# 一个很LOW的poc批量调用工具

## 工具描述
```
usage:
        pocscan.py [-s tyep:web | -l ./pocs] -i 127.0.0.1 -t 30

poc批量扫描工具,使用前建议先测试单个执行效果，个别插件非常耗时

optional arguments:
  -s SCRIPT, --script SCRIPT
                        "tyep:web app:zzcms || type:service:unauth"
  -l PATH, --load PATH  .py文件或目录，默认
  -i TARGET, --input TARGET
                        字符串、文本文件
  -t THREADNUM, --thread THREADNUM
                        多线程数，默认20
```
## 实例用法

```
# 加载指定路径脚本 
pocscan -l ./pocs/test.py -i 127.0.0.1 -t 20
# 加载指定目录下所有脚本 
pocscan -l ./pocs/ -i 127.0.0.1 -t 20
# 默认加载同目录下 pocs目录下的所有脚本 ，再通过-s 一些语法过滤
pocscan -s "type:web || type:service" -i 127.0.0.1 -t 20
# 多目标模式,加载IP.txt里的目标
pocscan -l ./pocs/test.py -i IP.txt -t 20

```
## poc插件模板
```
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

```
