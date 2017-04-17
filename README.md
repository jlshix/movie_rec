# movie_rec

毕业设计项目今天开始动手码代码

注释规范参见[这里](http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/)

## 17-04-08
- 建立项目目录
```shell
.
├── app     # 程序主目录
│   ├── __init__.py
│   ├── main    # 主蓝本
│   │   ├── errors.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   └── views.py
│   ├── models.py   # 数据库模型
│   ├── static      # 静态文件
│   ├── templates   # 模板
│   └── utils.py    # 工具
├── config.py       # 配置文件
├── db_operations   # 数据库脚本
├── README.md       # 说明
├── requirements.txt    # 包依赖
├── run.py          # 运行
├── tests           # 测试
├── venv            # 虚拟环境

```
- 使用两个蓝本：auth main
- 加入以下拓展
    - Flask-Bootstrap==3.3.7.1
    - Flask-Login==0.4.0
    - Flask-Script==2.0.5
    - Flask-SQLAlchemy==2.2
    - Flask-WTF==0.14.2
- 完成基本的注册登录功能(sqlite)
- TODO 密码散列

## 17-04-09
- 加入以下拓展：
    - Flask-Mail==0.9.1
    - Flask-Pymongo
- 增强密码安全性
- 用户确认邮件
- 接入 MongoDB
- 新增电影检索与添加

## 17-04-10
- debug 直接访问请求参数造成 400 错误的问题
- 新增 400 错误页面
- 新增 分页工具 paginate @main.utils
- 优化 分页导航展示
- 优化 搜索更改为按电影名称搜索
- 优化 搜索结果展示
- 新增 jinja2 macro 模板函数
- TODO MongoDB 查询与优化

## 17-04-11
- 新增 数据量达到 40k+

## 17-04-12
- 新增 数据量达到 48227 条

## 17-04-13
- 新增 API 蓝图 用于测试数据库操作

## 17-04-14

- 优化 将 SQLAlchemy 替换为 MongoEngine 全面使用 MongoDB

## 17-04-15
- 新增 电影展示页面
- 新增 用户展示页面

## 17-04-16
- 优化 用户数据模型


