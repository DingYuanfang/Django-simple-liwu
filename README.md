# Django-simple-liwu
Django 入门练习项目
# Introduce
这是我入门学习Django的第一个练习项目，模仿[Livety][1]网站写的
部署页面 [dingdemo.com:2016/liwu/acc][2]
入门学习使用的Django官方文档polls例子，所以附上了这个例子，方便学习参考。
# Install Requires
Python2.7 Django 1.7/1.9 已测试，其他版本未知
# Quic Strat
##一、安装
如果你使用最新版Django（1.9.4）那么你可以无需配置（其他版本未测试1.7貌似不行），即可运行这个app。
如果使用或需要迁移`liwu`，则需要按下列步骤配置

1.创建你的Django项目

    django-admin startproject mysite
    sudodjango-admin startproject mysite

2.copy `liwu` 这个文件夹到你的项目目录

##二、添加liwu进入项目配置

`conf：urls.py` 中加入

    url(r'^liwu/', include('liwu.urls')),

`settings.py` 下
STALLED_APPS常量中加入  `'liwu',`
MIDDLEWARE_CLASSES常量中注释掉`'django.middleware.csrf.CsrfViewMiddleware',`

##三、数据准备、生成模拟数据
###数据库初始化
    python manage.py makemigrations
    python manage.py migrate

###生成模拟数据

    python manage.py shell
    
    >>>from liwu.myfun import *
    
    >>>build_db_test()
    
    Build a complete^ ^
    
    >>>

##四、项目构建完成

访问主页http://127.0.0.1:8000/liwu/ac

注：
如果你需要改变主页http://127.0.0.1:8000地址，还需要修改一行代码。

liwu/templates/liwu/base.html文件

找到`var Absolute_PAth = "http://127.0.0.1:8000/liwu/acc"` 这行js代码
改为你需要的路径，例：

    var Absolute_Path = "http://dingdemo.com:2016/liwu/acc"


数据库使用默认sqlite3，测试配置mysql成功，其他未测试

参考：[Django1.8 Doc][3]




  [1]: http://www.livety.com/zh-hans/
  [2]: http://dingdemo.com:2016/liwu/acc
  [3]: http://python.usyiyi.cn/django/index.html#
