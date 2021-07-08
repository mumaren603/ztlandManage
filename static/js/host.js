window.onload = function () {
    /*----------------------权限获取-----------------------*/
    var auth = $('#queryBtn').attr('auth')
    console.log("当前登录人具有权限编码为：", auth, typeof (auth))

    var code_add = 'host_add'
    var code_edit = 'host_edit'
    var code_del = 'host_del'

    //根据后端返回权限码判断当前用户是权限访问
    if (auth.includes('auth_all')) {
        $('#addHostbtn').attr("style", "display:inline-block;")
        $('.edit_host_btn').attr("style", "display:inline-block;")
        $('.del_host_btn').attr("style", "display:inline-block;")
    }
    if (auth.includes(code_add)) {
        $('#addHostbtn').attr("style", "display:inline-block;")
    }
    if (auth.includes(code_edit)) {
        $('.edit_host_btn').attr("style", "display:inline-block;")
    }
    if (auth.includes(code_del)) {
        $('.del_host_btn').attr("style", "display:inline-block;")
    }
}

// 查询条件必填校验
function checkHost() {
    debugger;
    var intranetIP = $('#queryForm').find('input[name="intranetIP"]').val()
    var extrantIP = $('#queryForm').find('input[name="extrantIP"]').val()
    var serverType = $('#queryForm').find('select[name="serverType"]').val()
    var serverOs = $('#queryForm').find('select[name="serverOs"]').val()
    if ((intranetIP == undefined || intranetIP == '' || intranetIP == null) && (extrantIP == undefined || extrantIP == '' || extrantIP == null) && (serverType == undefined || serverType == '' || serverType == null) && (serverOs == undefined || serverOs == '' || serverOs == null)) {
        console.log("查询条件为空！")
        debugger;
        $('.verfity_div').removeClass('hide')
        $('#verfityInfo').text('请至少输入一个查询条件！')
        // 弹出框提示3秒后消失
        setTimeout(function () {
            $('.verfity_div').addClass('hide')
        }, 3000)
        $('#texts').html("")

        return false;     //返回false 页面将不会跳转。
    }
}


//添加
$('#addHostbtn').click(function () {
    $('.shadow,.add_div').removeClass('hide')
})

//添加取消
$('#add_cancel_btn').click(function () {
    $('.shadow,.add_div').addClass('hide')
})

//添加保存
$('#add_confirm_btn').click(function () {
    $.ajax({
        url: '/hostManage/host/add',
        type: 'POST',
        data: $('#add_form').serialize(),
        dataType: 'JSON',
        success: function (data) {
            debugger
            console.log(data, typeof (data))
            if (data.status == 0) {
                debugger
                location.reload()
            } else {
                debugger
                var error_obj = JSON.stringify(data.err_msg)  //转为字符串
                console.log('error_obj:', error_obj, typeof (error_obj))
                $.each($.parseJSON(error_obj), function (k, v) {  //后端传过来是json对象，前端需要转为js对象，需要做个转换JSON.parse() 或者 jQuery $.parseJSON()
                        console.log('#####', k, v)
                        // 如果前端值在后端处理有问题，那么通过弹出框显示错误信息
                        $('.verfity_div').removeClass('hide')
                        $('#verfityInfo').text(v)
                        // 弹出框提示3秒后消失
                        setTimeout(function () {
                            $('.verfity_div').addClass('hide')
                        }, 3000)
                    }
                )
            }
        }
    })
})


//编辑
$('.edit_host_btn').click(function () {
    debugger
    $('.shadow,.edit_div').removeClass('hide')

    //获取当前编辑所在行的字段值
    var h_id = $(this).parent().parent().attr('hid')
    var intranetIP = $(this).parent().parent().children('td[name="intranetIP"]').text()
    var extrantIP = $(this).parent().parent().children('td[name="extrantIP"]').text()
    var serverType = $(this).parent().parent().children('td[name="serverType"]').text()
    var serverPurpose = $(this).parent().parent().children('td[name="serverPurpose"]').text()
    var serverOs = $(this).parent().parent().children('td[name="serverOs"]').text()
    var serverAccount = $(this).parent().parent().children('td[name="serverAccount"]').text()
    var serverPassword = $(this).parent().parent().children('td[name="serverPassword"]').text()
    var originServer = $(this).parent().parent().children('td[name="originServer"]').text()

    //编辑框回填字段值
    $('#edit_form').find('input[name="s_id"]').val(h_id)
    $('#edit_form').find('input[name="intranetIP"]').val(intranetIP)
    $('#edit_form').find('input[name="extrantIP"]').val(extrantIP)
    $('#edit_form').find('select[name="serverType"]').val(serverType)
    $('#edit_form').find('input[name="serverPurpose"]').val(serverPurpose)
    $('#edit_form').find('select[name="serverOs"]').val(serverOs)
    $('#edit_form').find('input[name="serverAccount"]').val(serverAccount)
    $('#edit_form').find('input[name="serverPassword"]').val(serverPassword)
    $('#edit_form').find('input[name="originServer"]').val(originServer)
})

//编辑取消
$('#edit_cancel_btn').click(function () {
    $('.shadow,.edit_div').addClass('hide')
})

//编辑确定
$('#edit_confirm_btn').click(function () {
    $.ajax({
        url: '/hostManage/host/edit',
        type: 'POST',
        data: $('#edit_form').serialize(),
        dataType: 'JSON',
        success: function (data) {
            debugger
            console.log("后端返回数据：", data)
            if (data.status == 0) {
                debugger
                location.reload()
            } else {
                debugger
                var error_obj = JSON.stringify(data.err_msg)  //转为字符串
                console.log('error_obj:', error_obj, typeof (error_obj))
                $.each($.parseJSON(error_obj), function (k, v) {  //后端传过来是json对象，前端需要转为js对象，需要做个转换JSON.parse() 或者 jQuery $.parseJSON()
                    console.log('#####', k, v)
                    // 如果前端值在后端处理有问题，那么通过弹出框显示错误信息
                    $('.verfity_div').removeClass('hide')
                    $('#verfityInfo').text(v)
                    // 弹出框提示3秒后消失
                    setTimeout(function () {
                        $('.verfity_div').addClass('hide')
                    }, 3000)
                })
            }
        }
    })
})

//删除
$('.del_host_btn').click(function () {
    $('.shadow,.tips').removeClass('hide')

    //获取当前删除所在行的字段值
    var h_id = $(this).parent().parent().attr('hid')
    console.log("选中主机信息id为:", h_id)

    //将当前行id传递到弹出框中
    $('.tips').find('div[name="hid"]').val(h_id)
})

//删除取消
$('#delHostCancelBtn').click(function () {
    $('.shadow,.tips').addClass('hide')
})

//删除确定
$('#delHostConfirmBtn').click(function () {
    $.ajax({
        url: '/hostManage/host/del',
        type: 'POST',
        data: {'hid': $('.tips_footer').val()},
        dataType: 'JSON',
        success: function (data) {
            debugger
            console.log("后端返回数据：", data)
            if (data.status == 0) {
                debugger
                location.reload()
            } else {
                debugger
                var error_obj = JSON.stringify(data.err_msg)  //转为字符串
                console.log('error_obj:', error_obj, typeof (error_obj))
                $.each($.parseJSON(error_obj), function (k, v) {  //后端传过来是json对象，前端需要转为js对象，需要做个转换JSON.parse() 或者 jQuery $.parseJSON()
                    console.log('#####', k, v)
                    // 如果前端值在后端处理有问题，那么通过弹出框显示错误信息
                    $('.verfity_div').removeClass('hide')
                    $('#verfityInfo').text(v)
                    // 弹出框提示3秒后消失
                    setTimeout(function () {
                        $('.verfity_div').addClass('hide')
                    }, 3000)
                })
            }
        }
    })
})


