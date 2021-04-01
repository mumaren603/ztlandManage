'''校验模板，如环境详细信息校验模板，数据库校验模板'''
from django import forms

# 定义校验模板 -->环境详情界面编辑弹出框/添加弹出框提交时字段校验.
class envDetailInfoValidTemplate(forms.Form):
    service_chinese_name = forms.CharField(error_messages={'required': '服务名不可为空！'})
    service_name = forms.CharField(error_messages={'required': '服务标识不可为空！'})
    service_host = forms.GenericIPAddressField(error_messages={'required': 'IP地址不可为空！', 'invalid': 'IP地址格式错误！'})
    service_port = forms.IntegerField(max_value=65535,
                                      min_value=1,
                                      error_messages={'required': '服务端口不可为空！','max_value':'端口号不能大于65535！','min_value':'端口号不能小于1024！','invalid':'端口必须为数字！'}
                                      )
    service_model = forms.CharField(error_messages={'required': '所属节点不可为空！'})

# 定义添加主环境信息模板校验
class addEnvValidTemplate(forms.Form):
    frontIP = forms.GenericIPAddressField(error_messages={'required': '前端IP地址不可为空！', 'invalid': '前端IP地址格式错误！'})
    backIP = forms.GenericIPAddressField(error_messages={'required': '后端IP地址不可为空！', 'invalid': '后端IP地址格式错误！'})
    dbIP = forms.GenericIPAddressField(error_messages={'required': '数据库IP地址不可为空！', 'invalid': '数据库IP地址格式错误！'})
    env_name = forms.CharField(error_messages={'required': '所属环境不可为空！'})

# 定义校验模板 -->数据库详情界面编辑弹出框/添加弹出框提交时字段校验.
class dbDetailInfoValidTemplate(forms.Form):
    db_ip = forms.GenericIPAddressField(error_messages={'required': '数据库IP地址不可为空！', 'invalid': '数据库IP地址格式错误！'})
    db_port = forms.IntegerField(max_value=65535,
                                 min_value=1,
                                 error_messages={'required': '服务端口不可为空！','max_value':'端口号不能大于65535！','min_value':'端口号不能小于1024！','invalid':'端口必须为数字！'}
                                )
    db_sid = forms.CharField(error_messages={'required': '数据库实例不可为空！'})
    db_user = forms.CharField(error_messages={'required': '数据库用户名不可为空！'})
    db_password = forms.CharField(error_messages={'required': '数据库密码不可为空！'})