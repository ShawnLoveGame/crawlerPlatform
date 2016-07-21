# 百度登录
2016.07.21 alingse


实现wpa 端百度登录

## 文件结构

- `base.js` 提取出来的rsa加密部分代码（sorry，python 重写失败）
- `login.js` 用于加密的临时文件
- `login.py` 主文件
- `login_8c63308a.js` 百度加密js原始文件
- `requirements.txt`
- `login.xxxx.cookies` 这里是登录前load，登录成功后dump 的cookie，可以更安全，更快速吧至少。

### 其中js 文件关系是

`login_8c63308a.js ` 百度文件 -->  解压缩/反混淆 --> 

`base.js`  加密代码

`login.js` 程序运行时创建的临时文件，主要是base.js 和 调用加密打印的js代码

## jshell 说明

此处的 jshell 主要是用于 执行login.js脚本

手动处理为 `node login.js` 或`js login.js` 

此处的 `js` 我喜欢用 [`SpiderMonkey`](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey) 下面的 [`js-1.8.5`](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey/Releases/1.8.5) 版本 [(源代码下载目录)](http://ftp.mozilla.org/pub/js/)，体积小功能够，轻便。我在[crawler](https://github.com/alingse/crawler/) 项目 [dodata](https://github.com/alingse/crawler/tree/master/dodata)目录下编译了两个平台的二进制文件即`js-osx-amd64`和`js-linux64`

## 调用参数说明
  
  1. 如果安装有node 
  
  	`python login.py username password` 
  			
  2. 指定其他js解释器 
 
   `python login.py username password -j ../../../dodata/js-osx-amd64`
   

## NOTE

1. `login.py`中`baidu_login` 函数里 除了检测状态码 `400408` 之外就没有检测其他的了，比如密码出错，等问题
2. 验证登录成功没有做，可以考虑检测最后一步 `content` 内容
 

  


 