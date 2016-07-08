# 爬虫：国家食品药品监督管理总局


## 程序说明

1. search_key.py

   搜索关键字 searchpage 可以穿入 tableId 来改变搜索类目

2. item_detail.py

   根据上一步的id 拿到具体的表格，其实这个完全可以遍历把全部数据拿下来。


## 生成xls  

 ``cat key.id.info|python ../../dodata/jsoncsv.py|python ../../dodata/mkexcel.py > output.xls``

  