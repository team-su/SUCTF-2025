
过滤 UDP 流 ，右键 Decode as 将其解码为 RTP

![](resources/796142f836b6b9175147f35afd9b44bb.jpeg)

在 电话 -> RTP -> 中选择 RTP 播放器播放音频

![](resources/b8f79e51e5a4f38cae1cf4bf80ef0173.jpeg)

听出或者使用 ASR 转录工具得到以下信息： 

```txt
员工A：小李，你知道老板的电脑密码吗？我需要访问一些重要文件。
Employee A: Xiao Li, do you know the boss's computer password? I need to access some important files.

员工B：哈哈，老板的密码总是很简单。他经常用同一个密码。
Employee B: Haha, the boss's password is always simple. He often uses the same one.

员工A：真的吗？那重要文件的密码呢？
Employee A: Really? What about the password for important files?

员工B：如果是重要文件，他通常会在后面加上8个8。别忘了，老板的工号是1003。
Employee B: If it's an important file, he usually adds eight 8s at the end. Don't forget, the boss's employee number is 1003.
```

随即使用 sipdump 和 sipcrack 破解流量包中关于1003的用户密码

![](resources/8212a3d2a5fb390bef32f4f85781545a.jpeg)

![](resources/c53b56a8d0087fa46c45fc4be441f597.jpeg)

破解后得到老板的密码是 "verde351971" ，按照前文的提示组合得到密码 "verde35197188888888"

过滤 sip 协议找到一段 1003 和1004 的 sip 信息发送记录

![](resources/ec7e86b3324fc7b3ba6835ca1ded5667.jpeg)

跟踪流打开发现一段可疑的base64编码，并且最终文件是一个压缩包

![](resources/1a2d296eb7142819a1f782f38a81d740.jpeg)

使用前面得到的密码 verde35197188888888 将文件解压后得到一个 tls 证书 *(解压需要使用最新的nanazip或者支持zstd压缩算法的压缩软件)* 

![](resources/e66620980fe10210c91ed205be6e0de7.jpeg)

将该证书导入到 wireshark 中解密加密流量后过滤 sip 协议

![](resources/6215a81a3f7119aa3d8178e56c9e40ce.jpeg)

在电话中分析 sip 流量握手包，抓取 srtp 的加密密钥

![](resources/90cc7ae23df2c8f15a35483fe0f1a32f.jpeg)

找到对应的握手流

![](resources/4265e6e1732d62273baf630d5d014747.jpeg)

定位密钥

![](resources/784a1fcb0f7d7e123d50b2485facb252.jpeg)

使用密钥解密流量

![](resources/d0d32b7bb187e53d623fa9ffaa393aa3.jpeg)

解密后得到 hex 文件，将 hex 文件导入到 wireshark 中打开

![](resources/ba2dd3afb6361875804d2161875a9aff.jpeg)

![](resources/814afac153e9d0f4a9847b38dfcfb2fd.jpeg)

播放流

![](resources/2bc477708290972a6824d3eca5dd191e.jpeg)

从对话结果中梳理出以下逻辑
```txt
1老板：你好，王先生，感谢你今天能过来讨论我们的供货合同。
Boss: Hello, Mr. Wang, thank you for coming to discuss our supply contract today.

2供应商：您好，很高兴能再次合作。我们这次的报价和交货时间都做了一些调整，希望能更符合您的需求。
Supplier: Hello, it's a pleasure to work together again. We've made some adjustments to our pricing and delivery schedule this time, hoping to better meet your needs.

3老板：好的，我刚好在记录一些重要信息，请稍等……（开始在键盘上敲打）
Boss: Okay, I'm just recording some important information, please hold on... 

4供应商：当然，您请便。
Supplier: Of course, please go ahead.


按键58912598719870574


5老板：（一边敲打键盘一边说）抱歉，我正在记录一组密码，您知道的，现在信息安全很重要。
Boss: (while typing) Sorry, I'm recording a password, you know, information security is very important nowadays.

6供应商：是的，安全问题不容忽视。
Supplier: Yes, security issues cannot be ignored.

7老板：我最近发现我原来的密码使用方法不太安全，现在我喜欢用记录的密码和常用密码组合起来，然后进行哈希运算作为我机密文件的密码，这样就更安全了。
Boss: I recently discovered that my original way of using passwords wasn't very secure. Now I like to combine recorded passwords with common ones and then hash them to use as passwords for my confidential files, making it more secure.

8供应商：这是个好主意，能有效提升安全性。
Supplier: That's a good idea, it can effectively enhance security.

9老板：没错，这样即使有人知道了其中一个密码，也无法轻易破解我的账户。
Boss: Exactly, this way, even if someone knows one of the passwords, they can't easily crack my account.
```

接下来使用语法 `rtpevent and rtp.marker ==1` 过滤老板在对话时按键的信息

![](resources/e94b842698d07696699fb1f983918c34.jpeg)

得到58912598719870574，再利用老板的密码组合得到 `58912598719870574verde351971` ，进行哈希运算后得到密码 5c0b1d057aa7d5e9f7b2b10387f58540e2a6f9fc82ccb5d5f3cb2915aa0d1f77

![](resources/0847a71ccbf5cd3b6ae1327d30d4dab4.jpeg)

从http协议导出flag压缩包

![](resources/10f83e5689524ce30a2411fb61ae5c57.jpeg)

使用该密码解压压缩包得到flag

![](resources/c8cb0ab06914da91a12ca1d2e1adff05.jpeg)