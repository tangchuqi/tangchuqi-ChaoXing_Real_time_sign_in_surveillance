超星自动签到

见文章https://blog.csdn.net/kangqiao0422/article/details/104768092

本代码只是对上文的代码进行了修改（可以同时对多个课程同时监控）

运行环境和如何获取Cookie见上文

无需填入uid

本机运行环境 Python3.7.5，Windows 7 64位，，理论上Py3.6都行
运行py文件需要保证能import如下：requests json time random unicodedata os
已打包exe，在py（或者exe）文件旁边新建config.ini文件，内容如下
```json
{
  "Cookie": "",
  "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 ChaoXingStudy/ChaoXingStudy_3_4.3.2_ios_phone_201911291130_27 (@Kalimdor)_11391565702936108810"
}
```

在引号里面写上浏览器中获取来的Cookie值，例如
```json
{
	"Cookie":"uname=xxx; lv=xxx; fid=xxx; _uid=xxx; uf=xxx; _d=xxx; UID=xxx; vc=xxx; vc2=xxx; vc3=xxx; xxtenc=xxx; DSSTASH_LOG=xxx; k8s=xxx; route=xxx",
	"User-Agent":"Mozilla/5.0 (iPad; CPU OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 ChaoXingStudy/ChaoXingStudy_3_4.3.2_ios_phone_201911291130_27 (@Kalimdor)_11391565702936108810"
}
```
运行记录保存在log.txt内
新增微信推送，方法如下
```
首先在 http://sc.ftqq.com/3.version  用github登入
登入后 http://sc.ftqq.com/?c=code  打开这个网页有个SCKEY 一大串字符串
然后打开 http://sc.ftqq.com/?c=wechat&a=bind  进行微信绑定，作用是签到成功server酱通知你
```
监控时间建议别太短也别太长，自行设定或者默认都行
根据自己老师平时签到时间定。我们基本上是30-60分钟的签到（仅普通签到和手势签到和位置签到）
6~8分钟适合于10分钟的签到
可以自己修改列表成自己的常用的列表和间隔时间 去掉输入，然后用windows自带的"计划任务"准点调用py或者exe程序运行 
