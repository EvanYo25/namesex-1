namesex
========
"NameSex"，中文姓名的性別辨識：以中文名字判斷性別的 Python 套件。

"NameSex", Gender Classification by Chinese Name.

特點
========
* 共有四種基本判別方法：
    * Frequency 搭配 Logistic_Regression；
    * Frequency 搭配 KNN；
    * Word2Vec 搭配 Logistic_Regression ;
    * Word2Vec 搭配 KNN 。

* 可選擇上述四種判別方法的其中兩種，以自訂權重來作為判斷依據。
* 可選擇回傳性別或性別的機率。
* 可選擇只輸入名字；也可以選擇輸入姓氏加名字。中文姓名長度不一，若選擇是輸入姓氏加上名字，則名字部分的判斷為：姓名兩個字的，則以後面的字作為名；若姓名為三個字以上的，則以最後面的兩個字為名。

安裝說明
=======
請使用python3

* 安裝: `pip install namesex` / `pip3 install namesex`
* 透過 `import namesex` 來引用

演算法
========
* 使用公開的資料作為 training 的資料: 如高中榜單，共10,730筆 (姓名/性別)。
* Logistic Regression 以及 KNN 的部分使用 scikit-learn 套件。
* 使用兩種方法將中文名字轉換成 scikit-learn 可使用的陣列：
    * Frequency：以 training 資料出現過的所有字作為base vector(長度為1411)，若名字中有出現該字則為1，否則為0。
    * Word2Vec：以 w2v 套件將名字轉換成 vector，w2v 的訓練素材為2005年到2012年的網路新聞 。
* 本套件的四個基本判別法為上述兩點的交叉使用。
* 將全部資料做ten fold的數據：
	* The average of freq_log:
		accuracy= 0.9063373718546133
		precision= 0.8973043381833419
		recall= 0.9087089264735976
		f1= 0.9029346060218677
	* The average of freq_knn:
		accuracy= 0.8054986020503263
		precision= 0.917063618687054
		recall= 0.6532372247655946
		f1= 0.7626419804558757
	* The average of w2v_log:
		accuracy= 0.8303866949719098
		precision= 0.8398104474030846
		recall= 0.8224754165347242
		f1= 0.8309414457281269
	* The average of w2v_knn:
		accuracy= 0.778982477334303
		precision= 0.8619995068096357
		recall= 0.6717780614227171
		f1= 0.754990867890967
	* The average of 0.25 w2v_log + 0.75 freq_log:
		accuracy= 0.9051119503641759
		precision= 0.9001859709254456
		recall= 0.9140303835651732
		f1= 0.9069861748844597


主要功能
=======
1. 以預設的混合比例判斷中文名字的性別
----------------
* `ns.predict` 接受一個參數：即一串名字的list。將回傳一個對應的預測性別的list。 1代表男性，0代表女性。
* `ns.predict_prob` 接受一個參數：同樣為一串名字的list。但將回傳一個對應的預測性別機率的list。 list中每一項的前面為女生的機率，後面為男生的機率。
* 注意：中文名字需要是 UTF-8 編碼，若為 unicode 編碼可先使用 notepad++之類的編輯器轉成 UTF-8 編碼。
預設是使用 freq_log & w2v_log 分別以 0.75 及 0.25 的混合比例做為預測。

使用範例:

```python
# encoding=utf-8
import namesex
ns = namesex.NameSex()

ex1 = ns.predict(['王大明','李小美'])
print(ex1)
ex2 = ns.predict_prob(['王大明','李小美'])
print(ex2)

```

輸出:
  
    [ 1.  0.]

	[[ 0.26048166  0.73951834]
	 [ 0.90355755  0.09644245]]


2. 以自訂的模式或比例判斷中文名字的性別
----------------
* `ns.uni_model`接受兩個參數：第一個參數即一串名字的list，將回傳一個對應的預測性別的list；第二個參數為選擇的模式，使用者可以指定自己所欲使用的模式。
* 共有freq_log, freq_knn, w2v_log, w2v_knn 四種模式可選擇：
  freq_log => frequency 搭配 logistic regression
  freq_knn => frequency 搭配 knn
  w2v_log  => word2vector 搭配 logistic regression
  w2v_knn  => word2vector 搭配 knn

* `namesex.NameSex()`接受五個參數，只是我們在第一部分都是使用預設的：參數依序是模式一、模式二、模式一所占比例、模式二所佔比例、要預測的資料是否包含姓氏(預設為0，包含姓氏；可更改為1，不包含姓氏。)。

使用範例:

```python
# encoding=utf-8
import namesex

ns = namesex.NameSex()
# 使用freq_log的模式來預測
ex3 = ns.uni_model(['王大明','李小美'],"freq_log")
print(ex3)

ns2 = namesex.NameSex("w2v_knn","w2v_log",0.8,0.2,1)
ex4 = ns2.predict_prob(['大明','小美'])
print(ex4)

```

輸出:
  
	[[ 0.32732295  0.67267705]
	 [ 0.87141058  0.12858942]]

	[[  1.19915589e-02   9.88008441e-01]
	 [  9.99999694e-01   3.06260518e-07]]

--------------------
