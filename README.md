# toupi

2022.2.10 忘记同步服务器了 下次一定

2022.2.13 今天迈出了重要一步 为网站能正常访问做出了不可磨灭的贡献 熟练使用了连表查询 做出了一个用于翻页的接口 基本一次成型 
为我主页功能做出了调整 右边又来热榜功能 方便遍历阅读 以及图片可以正常访问 很好 下次要实现的功能先做出预期 要有用户的概念 什么是用户的概念 先从简单的做 为用户储存一个 上次的浏览记录 并且在主页增加一个一键到达上次储存浏览记录的按钮 这个按钮不再是a标签 要好看 大 圆滑 好 

2022.2.17 距离上次做了两个未带完成的功能 一个是搜索 搜索使用了双接口调用 一个是index页面的post 请求 采用表单的方式传递数据 page默认0 页面上做了漂亮的选框和输入框 采用request.form.get（）取值
很方便，在get请求上 采用和大网站一样的方式 主要是为了轻松实现翻页功能留下的接口 方便传递page 在sql语句上pysql like查询应该采用curs.execute(a,('%'+keyword+'%'))这样就不会出现数据库'keyword’为单独字符串问题 百分号成功被接纳 limit和page的强强搭配 就不用多少了 limit %s,10 轻松 现在因为小说太少 所以翻页一时半会在这个方面用不到 所以就没做 反正聪明人会自己输入网址翻页 笨的就不说了
 在novel上面如期的做了一个悬浮栏用来 实现一些功能 现在只有一个 为书保存书签 虽然现在是本地保存localStorage 能有5m大小 简直充足 但是不排除后期和线上兼容的问题，顺带一提 index页面用户没有访问我站书签的功能 下次一定补上 还有 没有同步服务器 很重要！！！
