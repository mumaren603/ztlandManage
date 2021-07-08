window.onload = function () {
    /*----------------------权限获取-----------------------*/
    var auth = $('#addEnvInfo').attr('auth')
    console.log("当前登录人具有权限编码为：", auth, typeof (auth))

    var code_add = 'env_add'
    var code_edit = 'env_edit'
    var code_del = 'env_del'

    //根据后端返回权限码判断当前用户是权限访问
    if (auth.includes('auth_all')) {
        $('#addEnvInfo').attr("style", "display:inline-block;")
        $('.edit_env_btn').attr("style", "display:inline-block;")
        $('.del_env_btn').attr("style", "display:inline-block;")
    }
    if (auth.includes(code_add)) {
        $('#addEnvInfo').attr("style", "display:inline-block;")
    }
    if (auth.includes(code_edit)) {
        $('.edit_env_btn').attr("style", "display:inline-block;")
    }
    if (auth.includes(code_del)) {
        $('.del_env_btn').attr("style", "display:inline-block;")
    }

}

// 查询条件必填校验
function checkEnv() {
    debugger;
    var searchParam = $('#searchParam').val()
    console.log('searchParam:',searchParam)
    if (searchParam == undefined || searchParam == '' || searchParam == null){
        console.log("查询条件为空！")
        debugger;
        $('.verfity_div').removeClass('hide')
        $('#verfityInfo').text('请输入查询条件！')
        // 弹出框提示3秒后消失
        setTimeout(function () {
            $('.verfity_div').addClass('hide')
        }, 3000)
        $('#texts').html("")

        return false;     //返回false 页面将不会跳转。
    }
}


/*主环境信息添加，编辑，删除*/
//添加
$('#addEnvInfo').click(function () {
    $('.shadow,.add_div').removeClass('hide')
})

//添加取消
$('#add_cancel_btn').click(function () {
    $('.shadow,.add_div').addClass('hide')
})

//添加保存
$('#add_confirm_btn').click(function () {
    $.ajax({
        url: '/envManage/env/add',
        type: 'POST',
        data: $('#add_form').serialize(),
        dataType: 'JSON',
        success: function (data) {
            console.log(data, typeof (data))
            if (data.status == 0) {
                location.reload()
            } else {
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


                /*
               $.each($.parseJSON(error_obj),function(k,v){  //后端传过来是json对象，前端需要转为js对象，需要做个转换JSON.parse() 或者 jQuery $.parseJSON()
                   var tag = document.createElement('span');
                   tag.className='error-msg';
                   tag.innerHTML = v[0];
                   $("input[name='"+k+"']").after(tag);
                   }
               )
                 */
            }
        }
    })
})

//编辑
$('.edit_env_btn').click(function () {
    $('.shadow,.edit_div').removeClass('hide')
    debugger

    //获取当前编辑所在行的字段值
    var h_id = $(this).parent().parent().attr('hid')
    var frontIP = $(this).parent().parent().children('td[name="frontIP"]').text()
    var backIP = $(this).parent().parent().children('td[name="backIP"]').text()
    var dbIP = $(this).parent().parent().children('td[name="dbIP"]').text()
    var env_name = $(this).parent().parent().children('td[name="env_name"]').text()
    var status = $(this).parent().parent().children('td[name="status"]').text()

    debugger
    //编辑框回填字段值
    $('#edit_form').find('input[name="s_id"]').val(h_id)
    $('#edit_form').find('input[name="frontIP"]').val(frontIP)
    $('#edit_form').find('input[name="backIP"]').val(backIP)
    $('#edit_form').find('input[name="dbIP"]').val(dbIP)
    $('#edit_form').find('input[name="env_name"]').val(env_name)
    $('#edit_form').find('input[name="status"]').val(status)
})

//编辑取消
$('#edit_cancel_btn').click(function () {
    $('.shadow,.edit_div').addClass('hide')
})

//编辑确定
$('#edit_confirm_btn').click(function () {
    $.ajax({
        url: '/envManage/env/edit',
        type: 'POST',
        data: $('#edit_form').serialize(),
        dataType: 'JSON',
        success: function (data) {
            console.log("后端返回数据：", data)
            if (data.status == 0) {
                location.reload()
            } else {
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
$('.del_env_btn').click(function () {
    $('.shadow,.tips').removeClass('hide')

    //获取当前删除所在行的字段值
    var h_id = $(this).parent().parent().attr('hid')
    console.log("环境主信息删除行id为:", h_id)

    //将当前行id传递到弹出框中
    $('.tips').find('div[name="hid"]').val(h_id)
})

//删除取消
$('#delEnvCancelBtn').click(function () {
    $('.shadow,.tips').addClass('hide')
})

//删除确定
$('#delEnvConfirmBtn').click(function () {
    $.ajax({
        url: '/envManage/env/del',
        type: 'POST',
        data: {'hid': $('.tips_footer').val()},
        dataType: 'JSON',
        success: function (data) {
            console.log("后端返回数据：", data)
            if (data.status == 0) {
                location.reload()
            } else {
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



