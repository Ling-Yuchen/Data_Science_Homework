# 关于数据科学基础司法大数据分析大作业



### 几个主要的模块



#### 网络爬虫

###### @马宇森 有空写一下



#### 中文分词

本次大作业采用了LTP分词工具，需要本地有python的运行环境

在cmd命令行界面输入命令：pip install ltp 进行安装

```python
# TextNLP.py
# -*- coding: utf-8 -*-
import re
import sys
from ltp import LTP

# TextNLP.py的主方法
def nlp(text):
    # 初始化ltp
    ltp = LTP()

    # 在对样例直接进行分词时，发现效果并不理想
    # 有许多我们希望得到的专有名词，例如：法院名称，公司名称，地址名称等会被拆分开
    # 考虑到问题的复杂性和程序的复杂性，在这里没有选择机器学习等高级方法，选择使用添加自定义词典的方式
    # 使用正则先从目标文本中筛选出我们想要的专有名词（具体实现见代码），加入到分词的自定义词典中
    my_word_list = gen_my_word_list(text)
    ltp.add_words(words=my_word_list, max_window=4)

    # 分词
    # segments 是包含所有分词结果的 list
    # part_of_speech 是分词结果中每个词对应词性的 list
    seg, hidden = ltp.seg([text])
    part_of_speech = ltp.pos(hidden)[0]
    segments = seg[0]
	
    # 根据 segments和对应的 part_of_speech 进一步筛选出我们想要的内容
    # nlp_result是一个list,分别包含了noun、verb、name和time这4个list
    nlp_result = gen_nlp_result(segments, part_of_speech)
    
	# 将得到的结果按某种形式输出
    # 本地服务器将会拿到这个输出流

# 执行入口
if __name__ == '__main__':
    if len(sys.argv) > 1:
        nlp(sys.argv[1])
    else:
        # 进行本地测试
        nlp("本地测试文本")
```

有关分词的具体内容参考：https://ltp.readthedocs.io/zh_CN/latest/



#### 客户端页面

html + css (bootstrap) + javascript (jquery)

页面布局和美化等可以后期再打磨

###### 主要的交互功能：

##### ① 上传本地文件

已实现文件上传，并可保存至./public/file目录下

ps：保存的文件名由随机数生成

```js
var express = require('express');
var path = require('path')
var fs = require("fs");
var multer  = require('multer');
 
var app = express();
//指定静态文件位置
app.use(express.static(path.join(__dirname, 'public')))
//上传之后放在工作目录下的 tmp 目录下。 上传的时候上传控件的name 必须是  image
app.use(multer({ dest: path.join(__dirname, 'tmp') }).array('image'));
 
//获取后缀名
function getExtName(fileName){
    var index1=fileName.lastIndexOf(".");
    var index2=fileName.length;
    var extName=fileName.substring(index1+1,index2);
    return extName;
}
 
app.post('/uploadPhoto', function (req, res) {
   //获取上传文件的后缀名
   var extName = getExtName(req.files[0].originalname);
    
   //随机数
   var rundomNumber = Math.ceil(Math.random()*10000000);
   //以随机数作为文件名
   var randomFileName =  rundomNumber + "."+extName;

   //创建文件目录
   var fileFolder = __dirname + "/public/file/";
//    if(!fs.exists(fileFolder))
//        fs.mkdir(fileFolder);
    
   //文件路径
   var fileFile = __dirname + "/public/file/" + randomFileName;
    
   //上传临时文件的路径
   var uploadedTempFilePath = req.files[0].path;
    
   //读取临时文件
   fs.readFile( uploadedTempFilePath, function (err, data) {
       //读取成功之后，复制到文件路径
        fs.writeFile(fileFile, data, function (err) {
            //写成功之后，返回 file元素显示上传之后的图片
              res.writeHead(200, {'Content-Type': 'text/html'});
              res.end("Save successfully!");
       });
   });
})
  
var server = app.listen(8088);
```



##### ② 接收服务器传回来的分词结果并将其可视化生成选项

还没做......

##### ③ 保存文件和标注

使用Blob对象实现

什么是Blob对象：https://zhuanlan.zhihu.com/p/161000123

```HTML
<script>
    $(function() {
        // 点击按钮保存提取的案件信息.json文件到本地
        $("input#saveLabel").click(function() {
            const data = generateData();
            var content = JSON.stringify(data);
            const blob = new Blob([content], { type: "text/plain; charset=utf-8" });
            const a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = "案件信息提取.json";
            a.click();
            URL.revokeObjectURL(a.href);
            a.remove();
        });

        // 点击按钮保存输入的案件信息.txt文件到本地
        $("input#saveText").click(function() {
            const data = getCaseText();
            if (data == "") {
                alert("没有已输入的案件信息！");
                return;
            }
            const blob = new Blob([data], { type: "text/plain; charset=utf-8" });
            const a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = "案件信息.txt";
            a.click();
            URL.revokeObjectURL(a.href);
            a.remove();
        });
    });
</script>
```



#### 本地服务器搭建

本次大作业我们采用 node.js 搭建本地服务器

官方下载安装：https://nodejs.org/en/download/

###### @胡睿 有空写一下



#### 客户端、服务器和pyhton脚本间的数据传输

本次大作业采用 WebSockect 协议进行客户端和服务器端的通讯

参考：https://zhuanlan.zhihu.com/p/97336307

前端 js 代码：

```javascript
    // 打开一个WebSocket:
    var ws = new WebSocket('ws://localhost:3000');
    
    //open event
    ws.onopen = function() {
        console.log("open websocket...");
    };
    
    //close event
    ws.onclose = function() {
        console.log("close websocket...");
    };
    
    // 响应onmessage事件:
    ws.onmessage = function(msg) { 
        // 这里可以处理接收到服务器的数据
        // 本次大作业中，需要接收服务器传回来的分词结果并将其可视化生成选项
    };

    $(function() {
        $("aButton").click(function() {
            // 点击按钮向服务器发送数据
            ws.send("some message");
        });
    });
```

后端 js 代码：

```javascript
const WebSockect = require('ws')
const wss = new WebSockect.Server({port: 3000});
console.log("setup server...");

// 用于启动一个子进程执行python脚本
var exec = require("child_process").exec;
// 用于解决后端中文显示乱码问题
var iconv = require('iconv-lite');

wss.on('connection', function (ws) {
    console.log(`[SERVER] connection()`);
    ws.on('message', function (message) {
        console.log(`[SERVER] Received: ${message}`);
        // 执行本地python脚本
        exec('py .\\TextNLP.py '+ message, {encoding: "gbk"},
            (error,stdout,stderr) => {
            	if(stdout.length > 1) {
                	var result = iconv.decode(stdout, "GBK");
                    // 后端输出pyhton的stdout
                	console.log('python stdout:', result);
                    // 将python的输出发送给前端
                    // 注意exec方法中的这个匿名函数作为参数是一个没有返回值的函数
                    // 一定要在该函数体内将结果传给前端，否则将拿不到数据
                	ws.send(result, (err) => {
                    	if (err) console.log(`[SERVER] error: ${err}`);
                	});
            	} else console.log('you don\'t offer args');
            	if(error) console.info('stderr : '+ stderr); 
        });
    });
});
```

