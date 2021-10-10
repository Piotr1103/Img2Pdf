# PDF-Tools
以圖檔資料夾生成PDF檔、從其他PDF檔複製書籤列

Create PDF files from imgs and copy bookmarks


Img2Pdf:

	1. 將要組成PDF檔的圖檔放入同一個目錄。
	2. 為了排序，每個圖檔應依序使用阿拉伯數字作為檔名命名。
	3. 目錄名將作為輸出PDF的檔名。

	1. Put all the img files that are to consist a PDF file into the same directory.
	2. In order to access orderly, every img file should be named with indo-arabic numbers in order.
	3. The name of the directory will be used as the name of the output PDF file.

BookmarkCopier(src,dst,offset):
	1. 將帶有欲複製書籤列的PDF檔放在setbooklines的第一個參數
	2. 將目的PDF檔放在setbooklines的第二個參數
	3. 倘若目的PDF檔比原檔少2頁，第三個參數輸入2，多二頁輸入-2，不多不少輸入0

	1. Put the source PDF file of the bookmarks you want to copy as the first argument.
	2. Put the destination PDF file as the second argument.
	3. If you have the destination file 2 pages less than the source file, put 2 as the third argument; 2 pages more, put -2; nothing more or less, put 0.