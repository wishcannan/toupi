# toupi

2022.2.10 忘记同步服务器了 下次一定

2022.2.13 今天迈出了重要一步 为网站能正常访问做出了不可磨灭的贡献 熟练使用了连表查询 做出了一个用于翻页的接口 基本一次成型 
为我主页功能做出了调整 右边又来热榜功能 方便遍历阅读 以及图片可以正常访问 很好 下次要实现的功能先做出预期 要有用户的概念 什么是用户的概念 先从简单的做 为用户储存一个 上次的浏览记录 并且在主页增加一个一键到达上次储存浏览记录的按钮 这个按钮不再是a标签 要好看 大 圆滑 好 

2022.2.17 距离上次做了两个未带完成的功能 一个是搜索 搜索使用了双接口调用 一个是index页面的post 请求 采用表单的方式传递数据 page默认0 页面上做了漂亮的选框和输入框 采用request.form.get（）取值
很方便，在get请求上 采用和大网站一样的方式 主要是为了轻松实现翻页功能留下的接口 方便传递page 在sql语句上pysql like查询应该采用curs.execute(a,('%'+keyword+'%'))这样就不会出现数据库'keyword’为单独字符串问题 百分号成功被接纳 limit和page的强强搭配 就不用多少了 limit %s,10 轻松 现在因为小说太少 所以翻页一时半会在这个方面用不到 所以就没做 反正聪明人会自己输入网址翻页 笨的就不说了
 在novel上面如期的做了一个悬浮栏用来 实现一些功能 现在只有一个 为书保存书签 虽然现在是本地保存localStorage 能有5m大小 简直充足 但是不排除后期和线上兼容的问题，顺带一提 index页面用户没有访问我站书签的功能 下次一定补上 还有 没有同步服务器 很重要！！！
 
 2022.3.4这次更新做了书签功能 index页面有了书签功能 写这个时候发现index.js没更新 想起来用ajax做的 一会补上 顺带一提是做了一个页面用来学习如何上传文件 这个功能以前就想做的 先看功能本身 本质上就是设置好参数的高斯模糊 其中涉及噪声产生,再来看请求方面 request这个没想到浏览器挺好的 用起来也很方便  
 <form method='post' enctype=multipart/form-data action="/upload">
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
轻松就实现了表单上传文件，后端flask 做了一个校验 防了一手有人在文件名上面做文章 来攻击服务器 from werkzeug.utils import secure_filename 这个里面的方法就是转义 / 以及\xf这种字符 防止对我文件结构搞破坏 然后还检查了一下后缀ALLOWED_EXTENSIONS = {'png','jpg','jpeg','bmp'}只想兼容这4种 不符合都用flash 准备返回一条消息 结果写到这发现前端根本没有接收 哈哈哈
1 <main>
2     {% for message in get_flashed_messages() %}
3         <div class="alert">{{ message }}</div>
4     {% endfor %}
5     {% block content %}{% endblock %}
6 </main>
这里贴上怎么用 不过都做了处理就是了，然后就是数据处理方面了 遭遇了 问题又cv2.imread 接受参数有限 不太能接受file对象 只能接受文件名 相对位置，采用python传统的#pip install Pillow
from PIL import Image ，image库解决了 然后就是cv2 储存时通道问题 众所周知cv2读取的通道不是rgb 而是bgr 所以这里可以采取更换通道的方式 或者直接用image库的img.save 当然我选择了后者 然后出乎意料的顺利呢 就把功能实现了 顺手解决了首页随机10本书的问题，只要刷新多就可以浏览全部书 不行就建议改网址 没想到有什么好的展示书的方式 不过我又留有select功能 给用户 所以应该问题不大 从这次起网站应该就是常驻了

