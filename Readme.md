带图片完整使用说明：[https://juejin.cn/spost/7427399875236855871](https://juejin.cn/spost/7427399875236855871) "同步小米笔记到电脑本地文件夹中"

该项目灵感来源([https://github.com/malinkang/weread2notion](https://github.com/malinkang/weread2notion) "将微信读书划线和笔记同步到Notion")
## 将小米笔记内容同步到obdisian
### 项目介绍
目前手机上使用的是小米笔记，非常喜欢小米笔记的摘录功能，电脑里使用ondisian整理所有的笔记，因此该项目主要功能是将小米笔记全部内容同步obsidian中
### 使用说明
1. star本项目
2. fork该项目
3. 获取小米云服务的cookie(MINOTE_COOKIE)
   - 登录<https://i.mi.com/>
   - 点击笔记，第一次登录可能需要验证码
   - 返回小米云笔记主页
   - 按F12进入开发者模式，依次点 Network -> Doc -> Headers-> cookie。复制 Cookie 字符串;
4. 设置本地储存目录(SAVE_DIR)
   - 找到Obsidian本地储存文件夹，我的是"D:\输出义务"
   - 在该文件夹下新建minote问价夹，之后的文件就会储存到"D:\输出义务\minote"文件夹中
5. 在Github的Secrets中添加以下变量
   - 打开你fork的工程，点击Settings->Secrets and variables->New repository secret
   - 添加以下变量
     - MINOTE_COOKIE
     - SAVE_DIR
6. 手动运行githubAction
   - 点击Action->minote sync->Run workflow -> Run workflow按钮
   - 观察运行状态，如果为绿色则运行成功，此时可以在设定好的本地文件夹中看到同步的笔记内容
