from PyPDF2 import PdfFileWriter,PdfFileReader

"""
f為書籤列所在檔案
obj為欲解析對象物件
lv為當前對象層級，用來搜尋整體物件層數
"""
#解析書籤列物件並且打印出來
def dechain(f,obj,lv):
	depth = lv
	if isinstance(obj,list):
		for i in obj:
			dechain(f,i,depth+1)
	else:
		print(lv*"\t"+"title="+obj['/Title'],end=', ')
		print("page="+str(f.getDestinationPageNumber(obj)+1),end='')
		if obj['/Type'] == '/XYZ':
			if isinstance(obj['/Top'],(float,int)):
				print(", top="+str(obj['/Top']),end='')
			if isinstance(obj['/Left'],(float,int)):
				print(",left="+str(obj['/Left']),end='')
		elif obj['/Type'] == '/FitH':
			print(",top="+str(obj['/Top']),end='')
		print()

#解析書籤列物件並且以字符串形式返回
def dechainwrite(f,obj,lv):
	depth = lv
	txt = ''
	if isinstance(obj,list):
		for i in obj:
			txt += dechainwrite(f,i,depth+1)
	else:
		txt += ("lv="+str(lv))
		txt += (", title="+obj['/Title'])
		txt += (", page="+str(f.getDestinationPageNumber(obj)+1))
		if obj['/Type'] == '/XYZ':
			txt += ", type=/XYZ"
			if isinstance(obj['/Top'],(float,int)):
				txt += (", top="+str(obj['/Top']))
			if isinstance(obj['/Left'],(float,int)):
				txt += (", left="+str(obj['/Left']))
		elif obj['/Type'] == '/FitH':
			txt += ", type=/FitH"
			txt += (", top="+str(obj['/Top']))
		else:
			txt += ", type=" + obj['/Type']
		txt += "\n"
	return txt

#取得書籤列物件
def getbooklines(filename):
	booklines = ''
	with open(filename, "rb") as f:
		pdf = PdfFileReader(f)
		bookmarks = pdf.getOutlines()
		for b in bookmarks:
			#解析層級從第0層開始
			c = dechainwrite(pdf,b,0)
			booklines += c
	return booklines

"""
getbooklines函數輸出的書籤列字串文件格式有以下兩種：
對齊縮放方式為/XYZ且帶有對齊座標參數:
	lv=層級, title=標題, page=頁數, type=/XYZ, top=距頂部距離, left=距左邊距離\n
對齊縮放方式為/XYZ不帶對齊座標參數:
	lv=層級, title=標題, page=頁數, type=/XYZ\n
對齊縮放方式為/FitH:
	lv=層級, title=標題, page=頁數, type=/FitH, top=距頂部距離\n
"""

#將書籤列加到另一個PDF檔上面
#offset是目的PDF檔比來源PDF檔多或少的頁面數量，少了2頁的話輸入2，多了輸入-2
def setbooklines(src,dst,offsets):
	#預設朝狀書籤列最多五層，設置一空數組以儲存父節點
	par = [None,None,None,None,None]
	#將輸入的來源PDF書籤列文件字串以行為單位分割
	b = getbooklines(src).split("\n")
	#去除書籤列文件尾部多餘的"\n"導致的空元素
	b.pop()
	
	#開啟PDF檔寫入類
	d = PdfFileWriter()
	p_src = PdfFileReader(open(src,'rb')).getNumPages()
	#從目標檔中讀取
	insrc = PdfFileReader(open(dst,'rb'))
	#將所有頁面依次傳入寫入類實例
	p_dst = insrc.getNumPages()
	
	if p_src!=p_dst and p_src-p_dst!=len(offsets):
		print("The page number of destination file is smaller than the source file.\nAnd the offset doesn't add up!\nMay cause Index out of list Error!")
	else:
		for i in range(p_dst):
			d.addPage(insrc.getPage(i))
		
		#方便提取文件格式中的內容，如'lv=1'，可取得1
		def gct(i):
			il = i.split("=")
			return il[1]
		
		#每一行的內容都以', '分隔，將內容取出後分別轉至合適型別
		for c in b:
			bookmark = c.split(", ")
			lv = int(gct(bookmark[0]))
			ttl = gct(bookmark[1])
			#輸出的頁數加過1，在這裡要減回去
			page = int(gct(bookmark[2]))-1
			
			"""
			倘若來源頁數比目標多，計算每個區段頁數的偏移量
			"""
			cursect = 0
			if offsets is not None:
				if page+1 in offsets:
					continue
				else:
					while page >= offsets[cursect]:
						cursect = cursect + 1
					page = page - cursect
					cursect = 0
			
			#取得對齊類型
			tp = gct(bookmark[3])
			#對齊縮放方式為/XYZ且帶有對齊座標參數top和left
			if tp=='/XYZ' and len(bookmark)==6:
				topc = (None if bookmark[4] is None else eval(gct(bookmark[4])))
				leftc = (None if bookmark[5] is None else eval(gct(bookmark[5])))
			#對齊縮放方式為/FitH，帶有對齊座標參數top
			elif tp=='/FitH' and len(bookmark)==5:
				topc = (None if bookmark[4] is None else eval(gct(bookmark[4])))
				leftc = None
			#對齊縮放方式為/XYZ不帶對齊座標參數top和left，將兩者設為None
			else:
				topc = None
				leftc = None
			
			#依照對齊座標參數決定寫入PDF的方式
			if tp == '/XYZ' and topc is not None and leftc is not None:
				cur = d.addBookmark(ttl,page,(None if lv==0 else par[lv-1]),None,False,False,'/XYZ',leftc,topc,None)
			elif tp == '/XYZ' and topc is None and leftc is None:
				cur = d.addBookmark(ttl,page,(None if lv==0 else par[lv-1]),None,False,False,'/XYZ',leftc,topc,None)
			elif tp == '/FitH':
				cur = d.addBookmark(ttl,page,(None if lv==0 else par[lv-1]),None,False,False,'/FitH',topc)
			elif tp == '/FitV':
				cur = d.addBookmark(ttl,page,(None if lv==0 else par[lv-1]),None,False,False,'/FitV',leftc)
			#為避免尚未考慮的對齊格式出現的預設處理
			else:
				print('Type undefined!')
			
			#將節點按階層加入數組，以儲存父節點
			par[lv] = cur
		#新的PDF檔以bookmarked.pdf為名輸出
		outputStream = open('bookmarked.pdf','wb')
		d.write(outputStream)
		outputStream.close()

#print(getbooklines('./pdf/A.pdf'))
#第21頁和第258頁被移除掉
#setbooklines('./pdf/A.pdf','./pdf/B.pdf',(21,258))
#目標和來源葉樹一樣時
setbooklines('./pdf/彝语简志.pdf','./pdf/彝语.pdf',None)