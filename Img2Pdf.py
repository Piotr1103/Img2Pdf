import os
import glob
from fpdf import FPDF

"""
為了按照順序寫入PDF檔，以數字為每個個別圖檔命名有利於讓程序依照順序讀取圖檔
計算機在排序時不看數值位數只看開頭，所以有必要將檔案的名稱在左邊補上0，否則10.jpg和100.jpg可能會被排在一起
"""

"""
#findPadLen函數用來找出所有檔明中的最大位數
#參數fmt可傳入元組
"""
def findPadLen(imgDir,fmt):
	il = glob.glob(f'{imgDir}/*.{fmt}')
	l = []
	"""
	glob.glob()函數取得的位址字串如下：
	目錄名稱\\001.副檔名
	"""
	for fn in il:
		s = fn.split('\\')
		#取得檔名本身
		l.append(s[-1])
	#依據名稱長度從數組中選出最長的檔名
	return len(max(l,key=len))

"""
#padFnLen函數將所有檔名按照目錄中的最大檔名位數來往左邊填補0
#參數fmt可傳入元組
"""
def padFnLen(imgDir,fmt):
	il = glob.glob(f'{imgDir}\\*.{fmt}')
	#最大檔名位數
	padLen = findPadLen(imgDir,fmt)
	
	for n in il:
		"""
		若檔名位數小於最大檔名位數則補上相應的0
		補完後再把目錄名、檔名、副檔名組合起來，然後對來源目錄裡的原檔進行改名
		"""
		#將路徑拆分開來
		s = n.split('\\')
		#檔名本身
		ns = s[-1]
		#去除檔名本身，只保留路徑前綴
		s.pop()
		#路徑前綴重新組合
		pre = "\\".join(s)
		
		if len(ns) < padLen:
			nn = pre + "\\" + ns.rjust(padLen,'0')
			os.rename(n,nn)

"""
#將圖檔寫入PDF檔的核心函數
#傳入的目錄名在本函數中還將作為輸出PDF的檔名
"""
def convert(imgDir,fmt,x=0,y=0,width='default',height='default'):
	nl = glob.glob(f'{imgDir}\\*.{fmt}')
	pdf = FPDF()
	"""
	w和h分別為圖檔寫入後的寬度和高度，預設為PDF檔頁面的寬和高
	x和y為圖檔距離PDF頁面左上角的相對座標
	"""
	w = pdf.w if width == 'default' else width
	h = pdf.h if height == 'default' else height
	
	for img in nl:
		pdf.add_page()
		pdf.image(img,x,y,w,h)
	pdf.output(f'{imgDir}.pdf',"F")

"""
#將所有函數整合起來方便操作
"""
def img2pdf(imgDir,fmt):
	findPadLen(imgDir,fmt)
	padFnLen(imgDir,fmt)
	convert(imgDir,fmt)

if __name__ == "__main__":
	print('本轉檔器一次只能合併同樣類型的圖檔，比如全部都是jpg檔。')
	print('下面請依序輸入所要轉檔的檔案所在目錄以及檔案類型。')
	imgDir = input('請輸入目錄名或地址；')
	fmt = input('請輸入來源檔案類型，不需要加點；')
	print('轉檔需要一些時間，請耐心等候……')
	img2pdf(imgDir,fmt)