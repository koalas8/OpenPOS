OpenPOS
=======

OpenPOS 是一套用来做会员卡管理，会员管理，库存管理（侧重于服装）的系统，使用Python语言编写，可跨平台运行。


安装方法
=======
* 1.安装第三方库：psycopg2, DBUtils, QRCode, xlwt, Flask, Pillow, sqlalchemy, flask-restful, google protobuf
* 2.安装数据库：postgreSQL 9.2+
* 3.创建数据库jf_card, 并执行DDL下的ddl.sql脚本和update_database.sql,使用init_database.sql初始化数据

运行
=======
启动server交易端和web后台,脚本分别为 angserver/server.py 和 angcard/run_locale.py

