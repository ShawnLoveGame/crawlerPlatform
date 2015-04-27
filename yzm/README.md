#bu hui markdown
##
###
1.getimg.py  
    download many yanzhengma (means verifycode in English)
2.if it's Binary Image ,nothing,
    else run doimg.py to trans image to Binary
3.makeyzm.py
    use K-means to split&save
    rename or mark the split image . edit the yzm.py for different length code
    you can edit the char_count (means 0-9=10,a-z=26)& char_max ( K-means K )
4.testyzm.py
  

5.add the dir ./training_data_select yzm.py and doimg.py to you project
