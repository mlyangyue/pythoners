#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Andy'
"""
用动态规划求出最长公共子列
初始化一个元素全是0的二位数组L,m和n分别从0开始，m++，n++循环,如果str1[m] == str2[n]，则L[m,n] = L[m - 1, n -1] + 1,
如果str1[m] != str2[n]，则L[m,n] = max{L[m,n - 1]，L[m - 1, n]}
最后从L[m,n]中的数字一定是最大的，且这个数字就是最长公共子序列的长度
"""

def lcs(str1,str2):
	len1 = len(str1)
	len2 = len(str2)
	L = [[0 for i in range(len2+1)] for j in range(len1+1)]
	flag = [[0 for i in range(len2+1)] for j in range(len1+1)]
	for i in range(1,len1+1):
		for j in range(1,len2+1):
			if str1[i-1] == str2[j-1]:
				L[i][j] = L[i-1][j-1] + 1
				flag[i][j] = 'ok'
			else:
				if L[i][j-1] >= L[i-1][j]:
					L[i][j] = L[i][j-1]
					flag[i][j] = 'left'
				else:
					L[i][j] = L[i-1][j]
					flag[i][j] = 'up'

	return L,flag

def printlcs(flag,str1,i,j):
	if i == 0 or j == 0:
		return
	if flag[i][j] == 'ok':
		printlcs(flag,str1,i-1,j-1)
		print str1[i-1],
	elif flag[i][j] == 'left':
		printlcs(flag,str1,i,j-1)
	else:
		printlcs(flag,str1,i-1,j)
if __name__ == "__main__":
	str2 = "ADCA"
	str1 = "ACBA"
	res,flag = lcs(str1,str2)
	for item in res:
		print item

	printlcs(flag,str1,len(str1),len(str2))