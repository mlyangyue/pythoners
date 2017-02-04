#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'


'''打包log'''
def tar_files(sdir,suffix):
    """
    :func   打包目标文件夹下的文件
    :param  sdir目标文件夹的绝对路径,  suffix 打包的后缀
    """
    import os
    from time import strftime
    time_suf = strftime("%Y%m%d%H%M%S")  # 格式化时间
    os.chdir(sdir) # 切换目录到目标文件夹下
    os.system("tar zcvf log_{time_suf}.tar.gz *{suffix}".format(time_suf=time_suf,suffix=suffix)) # 执行打包命令
    #os.system("rm -rf *{suffix}".format(suffix=suffix)) # 执行删除命令

if __name__=="__main__":
    tar_files("/Users/wangranming/myproject/logs",".log")

