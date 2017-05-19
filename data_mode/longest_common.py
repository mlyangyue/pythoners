#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
"""用二维数组的方式找到最长子串,以斜对角的值来筛选最长的公共子串"""


def find_common(str1,str2,qty):
	array = [[0 for j in str2] for i in str1]
	amax = 0
	end = 0
	for i in range(len(str1)):
		for j in range(len(str2)):
			if str1[i] == str2[j]:
				if i == 0 or j == 0:
					array[i][j] = 1
				else:
					array[i][j] = array[i-1][j-1]+1
				length = array[i][j]
				if length>=qty:
					amax = array[i][j]
					end = i + 1
	return str1[end - amax:end],amax




if __name__=="__main__":
	str1 = "123456789"
	str2 = "25678919"

	ret = find_common(str1,str2,2)
	print ret
