var express = require('express');
var path = require('path')
var fs = require("fs");
var multer  = require('multer');
 
var app = express();
//指定静态文件位置
app.use(express.static(path.join(__dirname, 'public')))
//上传之后放在工作目录下的 tmp 目录下。 上传的时候上传控件的name 必须是  image
app.use(multer({ dest: path.join(__dirname, 'tmp') }).array('image'));


const WebSockect = require('ws')
const wss = new WebSockect.Server({port: 3000});
console.log("setup server...");
 
//获取后缀名
function getExtName(fileName){
    var index1 = fileName.lastIndexOf(".");
    var index2 = fileName.length;
    var extName = fileName.substring(index1+1,index2);
    return extName;
}
 
app.post('/uploadFile', (req, res) => {
   //获取上传文件的后缀名
   var extName = getExtName(req.files[0].originalname);
    
   //随机数
//    var rundomNumber = Math.ceil(Math.random()*10000000);
   //以随机数作为文件名
   var randomFileName =  "case." + extName;
    
   //文件路径
   var fileFile = __dirname + "/public/file/" + randomFileName;
    
   //上传临时文件的路径
   var uploadedTempFilePath = req.files[0].path;
    
   //读取临时文件
   fs.readFile( uploadedTempFilePath, (err, data) => {
       //读取成功之后，复制到文件路径
        fs.writeFile(fileFile, data, (err) => {
            //写成功之后，返回 file元素显示上传之后的图片
            res.writeHead(200, {'Content-Type': 'text/html'});
            res.end("Save successfully!");
            // if (err) console.log(`[SERVER] error: ${err}`);
       });
   });
});

var exec = require("child_process").exec;
var iconv = require('iconv-lite');

wss.on('connection', (ws) => {
    console.log(`[SERVER] connection()`);
    
    ws.on('message', (message) => {
        var msg = new String(message);
        if (msg.startsWith("@show")) {
            fs.readdir(__dirname+"/public/file/", (err, files) => {
                files.forEach((file) => {
                    fs.readFile(__dirname+"/public/file/"+file, (err, data) => {
                        var fileData = iconv.decode(data, "UTF-8");
                        console.log(fileData); 
                        ws.send("@show"+ fileData, (err) => {
                            if(err) {
                                console.log(`[SERVER] error: ${err}`);
                            }
                        })
                    })
                });
            });
        }
        else {
            console.log(`[SERVER] Received: ${message}`);
            exec('py .\\TextNLP.py '+ message +' ', {encoding: "gbk"}, (error, stdout, stderr) => {
                if(stdout.length > 1) {
                    var result = iconv.decode(stdout, "GBK");
                    console.log('python stdout:', result);
                    ws.send("@nlp"+ result, (err) => {
                        if(err) {
                            console.log(`[SERVER] error: ${err}`);
                        }
                    });
                } else {
                    console.log('you don\'t offer args');
                }
                if(error) {
                    console.info('stderr : '+ stderr); 
                }
            });
        }
    });   
});
  
var server = app.listen(8088);