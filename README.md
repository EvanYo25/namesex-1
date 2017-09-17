namesex
========
"NameSex"，中文姓名的性別辨識：以中文名字判斷性別的 Python 套件。

"NameSex", Gender Classification for Chinese Name.

特點
========
* 共有四種基本判別方法：
    * Frequency 搭配 Logistic_Regression；
    * Frequency 搭配 KNN；
    * Word2Vec 搭配 Logistic_Regression ;
    * Word2Vec 搭配 KNN 。

* 可選擇上述四種判別方法的其中兩種，以自訂權重來作為判斷依據。
* 可選擇回傳性別或性別的機率。

安裝說明
=======

代码对 Python 2/3 均兼容

* 全自動安裝：`easy_install namesex` 或者 `pip install namesex` / `pip3 install namesex`
* 半自動安裝：先下下載 http://pypi.python.org/pypi/namesex/ ，解壓縮後執行 `python setup.py install`
* 手動安裝：將 namesex 目錄放置於當前目錄或者是 site-packages 目錄
* 透過 `import namesex` 來引用

演算法
========
* 中文姓名長度不一，若姓名為兩個字的，則以後面的字作為名；若名字為三個字以上的，則以最後面的兩個字為名。
* 使用公開的資料作為 training 的資料: 如高中榜單，共約10,000筆 (姓名/性別)。
* Logistic Regression 以及 KNN 的部分使用 scikit-learn 套件。
* 使用兩種方法將中文名字轉換成 scikit-learn 可使用的陣列：
    * Frequency：以 training 資料出現過的所有字作為base vector(長度為1411)，若名字中有出現該字則為1，否則為0。
    * Word2Vec：以 w2v 套件將名字轉換成 vector，w2v 的訓練素材為2005年到2012年的網路新聞 。
* 本套件的四個基本判別法為上述兩點的交叉使用。

主要功能
=======
1. 以預設的混合比例判斷中文名字的性別
----------------
* `ns.predict` 接受一個參數：即一串名字的list。將回傳一個對應的預測性別的list。 1代表男性，0代表女性。
* `ns.predict_prob` 接受一個參數：同樣為一串名字的list。但將回傳一個對應的預測性別機率的list。 list中每一項的前面為女生的機率，後面為男生的機率。
* 注意：中文名字需要是 UTF-8 編碼，若為 unicode 編碼可先使用 notepad++之類的編輯器轉成 UTF-8 編碼。
預設是使用 freq_log & w2v_knn 分別以 0.75 及 0.25 的混合比例做為預測。

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

    [[ 0.04290965  0.95709035]
     [ 0.98962959  0.01037041]]


2. 以自訂的模式或比例判斷中文名字的性別
----------------
* `ns.uni_model`接受兩個參數：第一個參數即一串名字的list，將回傳一個對應的預測性別的list；第二個參數為選擇的模式，使用者可以指定自己所欲使用的模式。
* 共有freq_log, freq_knn, w2v_log, w2v_knn 四種模式可選擇：
  freq_log => frequency 搭配 logistic regression
  freq_knn => frequency 搭配 knn
  w2v_log  => word2vector 搭配 logistic regression
  w2v_knn  => word2vector 搭配 knn

* `namesex.NameSex()`接受四個參數，只是我們剛剛都是使用預設的：參數依序是模式一、模式二、模式一所占比例、模式二所佔比例。

使用範例:

```python
# encoding=utf-8
import namesex

ns = namesex.NameSex()
# 使用freq_log的模式來預測
ex3 = ns.uni_model(['王大明','李小美'],"freq_log")
print(ex3)

ns2 = namesex.NameSex("freq_knn","w2v_log",0.8,0.2)
ex4 = ns2.predict_prob(['王大明','李小美'])
print(ex4)

```

輸出:
  
    [[ 0.0155462   0.9844538 ]
     [ 0.98617279  0.01382721]]

    [[  1.11260148e-02   9.88873985e-01]
     [  9.99999688e-01   3.12214177e-07]]

--------------------
