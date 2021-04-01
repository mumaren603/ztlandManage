项目若移至新目录，请先完成以下配置
1.创建mysql数据库，实例名：ztland，用户名/密码：root/root（注意与settings下配置保持一致）
2.models.py下为初始化用户表，需要创建
    python manage.py makemigrations
    python manage.py migrate
3.导入初始用户数据
insert into machine_userinfo values(1,'lls','123456','lls@163.com',null,null);
insert into machine_userinfo values(2,'admin','admin','root@qq.com',null,null);

4.导入业务数据
--machine_envinfo
insert into machine_envinfo values(1,'无锡环境','172.0.0.246','172.0.0.109','172.0.0.250','在用');
insert into machine_envinfo values(2,'泰州环境','172.0.0.248','172.0.0.203','172.0.0.250','在用');
insert into machine_envinfo values(3,'宜兴环境','172.0.0.245','172.0.0.108','172.0.0.250','在用');
insert into machine_envinfo values(4,'宿迁环境','172.0.0.200','172.0.0.201','172.0.0.250','在用');

--machine_envinfodetail
insert into machine_envdetailinfo values(1,'起步平台','Bex5_v3.8','172.0.0.246',8080,'D:/BeX5/Bex5_v3.8','http://172.0.0.246:8080','前端',SYSDATE(),SYSDATE(),'1');
insert into machine_envdetailinfo values(2,'起步授权服务','license','172.0.0.246',9090,'D:/BeX5/license_server','172.0.0.246:9090','前端',SYSDATE(),SYSDATE(),'1');
insert into machine_envdetailinfo values(3,'业务层','service-bizz','172.0.0.201',1102,'/opt/biz','172.0.0.201:1102','后端',SYSDATE(),SYSDATE(),'1');

--machine_dbinfo
insert into machine_dbinfo values(1,'172.0.0.250',1521,'orcldj','DJJGK','DJJGK','登记结果库',SYSDATE(),SYSDATE(),'1');
insert into machine_dbinfo values(2,'172.0.0.250',1521,'orcldj','XTPZK','XTPZK','登记结果库',SYSDATE(),SYSDATE(),'1');
insert into machine_dbinfo values(3,'172.0.0.247',1521,'tzdj','DJJGK','DJJGK','登记结果库',SYSDATE(),SYSDATE(),'2');