import os
import glob

imgDir = input("請輸入圖檔路徑：")
fmt = input("請輸入欲取得圖檔之格式，不加點：")

il = glob.glob(f'{imgDir}/*.{fmt}')
"""
glob.glob()函數取得的位址字串如下：
目錄名稱\\001.副檔名
"""
for fn in il:
	s = fn.split('\\')
	n = s[-1].split('-')[-1]
	s.pop()
	pre = '\\'.join(s)
	nn = pre + "\\" + n
	os.rename(fn, nn)

"""
考慮直接將原圖檔目錄在特定路徑上複製一個
"""