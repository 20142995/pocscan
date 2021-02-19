#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import re
import argparse
import time
import threading
import importlib.util
import queue as Queue

queue = Queue.Queue()

def load_plugin(_file):
    plugins = {}
    _name = os.path.splitext(os.path.basename(_file))[0] 
    try:
        _spec = importlib.util.spec_from_file_location(_name, _file)
        _module = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_module)
        if hasattr(_module,'poc'):
            plugins[_name] = _module.poc
            print(f"[+] load {_name} success",end='\r')
        else:
            print(f"[-] load {_name} failed :not found poc()")
    except Exception as e:
        print(f"[-] load {_name} failed :{e}")
    return plugins

def load_plugin_from_path(path):
    plugins = {}
    if os.path.isfile(path) and path.endswith('.py') and path != '__init__.py':
        plugins.update(load_plugin(path))
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for _file in files:
                if not _file.endswith('.py') or _file == '__init__.py':continue
                plugins.update(load_plugin(os.path.join(root,_file)))
    print('[+] load plugin over'+" "*50)
    return plugins

def exception_handled_function(thread_function, args=()):
    try:
        thread_function(*args)
    except KeyboardInterrupt:
        raise
    except:
        pass

def run_threads(num_threads, thread_function, args=()):
    threads = []
    for num_threads in range(num_threads):
        thread = threading.Thread(target=exception_handled_function, name=str(num_threads),
                                  args=(thread_function, args))
        thread.setDaemon(True)
        try:
            thread.start()
        except:
            break
        threads.append(thread)
    alive = True
    while alive:
        alive = False
        for thread in threads:
            if sys.version_info < (3, 9):
                _talive = thread.isAlive
            else:
                _talive = thread.is_alive
            if _talive():
                alive = True
                time.sleep(0.1)

def worker():
    while not queue.empty():
        name,poc,arg = queue.get()
        try:
            res = poc(arg)
            if res is False or res is None:
                # sys.stdout.write('[-]\t{}\t{}\n'.format(name,arg))
                pass
            elif res is True:
                sys.stdout.write('[{}]\t{}\n'.format(name,arg))
            else:
                sys.stdout.write('[{}]\t{}\n'.format(name,res))
        except:
            pass

def main():
    parser = argparse.ArgumentParser(description='poc批量扫描工具,使用前建议先测试单个执行效果，个别插件非常耗时',usage='\n\t{} [-s tyep:web | -l ./pocs] -i 127.0.0.1 -t 30 '.format(sys.argv[0]))
    parser.add_argument('-s',"--script",dest='script',help='"tyep:web app:zzcms || type:service:unauth"')
    parser.add_argument('-l','--load',dest="path",default="", help='.py文件或目录，默认')
    parser.add_argument('-i',"--input",dest='target',help='字符串、文本文件')
    parser.add_argument('-t','--thread',dest="threadNum",type=int,default=20, help='多线程数，默认20')
    
    args = parser.parse_args()
    if not args.target or (not args.script and not args.path):
        parser.print_help()
        sys.exit()
    if args.path:
        plugins = load_plugin_from_path(args.path)
        print(f'[+] load plugin number {len(plugins)}')
    else:
        tmp_plugins = load_plugin_from_path(os.path.join(os.path.abspath(os.path.dirname(__file__)),'pocs'))
        print(f'[+] load plugin number {len(tmp_plugins)}')
        plugins = {}
        for name,poc in tmp_plugins.items():
            for ks in args.script.split('||'):
                if all([re.search(k.strip(),str(poc.__doc__),re.I) for k in ks.split(' ') if k.strip()]):
                    plugins[name] = poc
    print(f'[+] use plugin number {len(plugins)} :{",".join(plugins.keys())}')
    targets = []
    if os.path.isfile(args.target) and args.target.endswith('.txt'):
        targets += [i.strip() for i in open(args.target,'r',encoding='utf8').readlines() if i.strip()]
    else:
        targets.append(args.target)
    print(f'[+] load target number {len(targets)}')
    for target in targets:
        for name,poc in plugins.items():
            queue.put((name,poc,target))
    total = queue.qsize()
    print(f'[+] task number {total}')
    run_threads(args.threadNum, worker)

if __name__ == "__main__":
    main()