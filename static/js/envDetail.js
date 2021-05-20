window.onload=function(){
/*----------------------权限获取-----------------------*/
    var auth = $('.content_header').attr('auth')
    console.log("当前登录人具有权限编码为：",auth,typeof(auth))

    var code_detail_add1 ='env_detail_server_add'
    var code_detail_add2 ='env_detail_db_add'
    var code_detail_edit ='env_detail_edit'
    var code_detail_del ='env_detail_del'

    //根据后端返回权限码判断当前用户是权限访问
    if (auth.includes('auth_all')){
        $('#addEnvDetailBtn').attr("style","display:inline-block;")
        $('#addDbDetailBtn').attr("style","display:inline-block;")
        $('.edit_envDetail_btn').attr("style","display:inline-block;")
        $('.edit_dbDetail_btn').attr("style","display:inline-block;")
        $('.del_envDetail_btn').attr("style","display:inline-block;")
    }
    if(auth.includes(code_detail_add1)){
        $('#addEnvDetailBtn').attr("style","display:inline-block;")
    }
    if(auth.includes(code_detail_add2)){
        $('#addDbDetailBtn').attr("style","display:inline-block;")
    }
    if(auth.includes(code_detail_edit)){
        $('.edit_envDetail_btn').attr("style","display:inline-block;")
        $('.edit_dbDetail_btn').attr("style","display:inline-block;")
    }
    if(auth.includes(code_detail_del)){
         $('.del_envDetail_btn').attr("style","display:inline-block;")
    }


    //不同业务端详细信息切换
    $('.menu_item').click(function(){
        $(this).addClass('active').siblings().removeClass('active');
        var target = $(this).attr('a');
        $('.content_b_c').children("[b='"+target+"']").removeClass('hide').siblings().addClass('hide');
    });

/*------------------编辑操作---------------------------*/
    //前端、后端、FTP、中间件 编辑按钮
    $('.edit_envDetail_btn').click(function () {
        $('.shadow,.edit_env_div').removeClass('hide')

        //获取当前编辑所在行的字段值
        var h_id = $(this).parent().parent().attr('hid')
        var node_id = $(this).parent().parent().attr('node')
        var service_chinese_name = $(this).parent().parent().children('td[name="service_chinese_name"]').text()
        var service_name = $(this).parent().parent().children('td[name="service_name"]').text()
        var service_host = $(this).parent().parent().children('td[name="service_host"]').text()
        var service_port = $(this).parent().parent().children('td[name="service_port"]').text()
        var service_url = $(this).parent().parent().children('td[name="service_url"]').text()
        var service_deploy_path = $(this).parent().parent().children('td[name="service_deploy_path"]').text()


        //编辑框回填字段值
        $('#edit_env_form').find('input[name="s_id"]').val(h_id)
        $('#edit_env_form').find('input[name="service_chinese_name"]').val(service_chinese_name)
        $('#edit_env_form').find('input[name="service_name"]').val(service_name)
        $('#edit_env_form').find('input[name="service_host"]').val(service_host)
        $('#edit_env_form').find('input[name="service_port"]').val(service_port)
        $('#edit_env_form').find('input[name="service_url"]').val(service_url)
        $('#edit_env_form').find('input[name="service_deploy_path"]').val(service_deploy_path)
        $('#edit_env_form').find('select[name="service_model"]').val(node_id)
    })

    //前端、后端、FTP、中间件编辑界面取消按钮
    $('#editEnvCancelBtn').click(function () {
        $('.shadow,.edit_env_div').addClass('hide')
    })

    //前端、后端、FTP、中间件编辑界面确定按钮
    $('#editEnvConfirmBtn').click(function(){
        $.ajax({
            url:'/envManage/env/detail/edit',
            type:'POST',
            data:$('#edit_env_form').serialize(),
            dataType:'JSON',
            success:function (data) {
                console.log(data,typeof(data))
                if(data.status == 0){
                    location.reload()
                }else {
                    var error_obj = JSON.stringify(data.err_msg)  //转为字符串
                    $.each($.parseJSON(error_obj),function(k,v){  //后端传过来是json对象，前端需要转为js对象，需要做个转换JSON.parse() 或者 jQuery $.parseJSON()
                        console.log(k,v)
                        // 如果前端值在后端处理有问题，那么通过弹出框显示错误信息
                        $('.verfity_div').removeClass('hide')
                        $('#verfityInfo').text(v)
                        // 弹出框提示3秒后消失
                        setTimeout(function (){$('.verfity_div').addClass('hide')},3000 )
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

    //数据库编辑按钮
    $('.edit_dbDetail_btn').click(function () {
        $('.shadow,.edit_db_div').removeClass('hide')

        //获取当前编辑所在行的字段值
        var db_id = $(this).parent().parent().attr('hid')
        var db_ip = $(this).parent().parent().children('td[name="db_ip"]').text()
        var db_port = $(this).parent().parent().children('td[name="db_port"]').text()
        var db_sid = $(this).parent().parent().children('td[name="db_sid"]').text()
        var db_name = $(this).parent().parent().children('td[name="db_name"]').text()
        var db_user = $(this).parent().parent().children('td[name="db_user"]').text()
        var db_password = $(this).parent().parent().children('td[name="db_password"]').text()

        console.log('db_ip',db_ip)
        console.log('db_id',db_id)

        //编辑框回填字段值
        $('#edit_db_form').find('input[name="db_id"]').val(db_id)
        $('#edit_db_form').find('input[name="db_ip"]').val(db_ip)
        $('#edit_db_form').find('input[name="db_port"]').val(db_port)
        $('#edit_db_form').find('input[name="db_sid"]').val(db_sid)
        $('#edit_db_form').find('input[name="db_name"]').val(db_name)
        $('#edit_db_form').find('input[name="db_user"]').val(db_user)
        $('#edit_db_form').find('input[name="db_password"]').val(db_password)
    })

    //数据库编辑界面取消按钮
    $('#editDbCancelBtn').click(function () {
        $('.shadow,.edit_db_div').addClass('hide')
    })

    //数据库编辑界面确定按钮
    $('#editDbConfirmBtn').click(function(){
        $.ajax({
            url:'/envManage/db/detail/edit',
            type:'POST',
            data:$('#edit_db_form').serialize(),
            dataType:'JSON',
            success:function (data) {
                console.log(data,typeof(data))
                if(data.status == 0){
                    location.reload()
                }else {
                    var error_obj = JSON.stringify(data.err_msg)  //转为字符串
                    $.each($.parseJSON(error_obj),function(k,v){  //后端传过来是json对象，前端需要转为js对象，需要做个转换JSON.parse() 或者 jQuery $.parseJSON()
                        console.log(k,v)
                        // 如果前端值在后端处理有问题，那么通过弹出框显示错误信息
                        $('.verfity_div').removeClass('hide')
                        $('#verfityInfo').text(v)
                        // 弹出框提示3秒后消失
                        setTimeout(function (){$('.verfity_div').addClass('hide')},3000 )
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


/*--------------删除操作--------------------*/
    //环境、数据库详细信息删除
    $('.del_envDetail_btn').click(function () {
        $('.shadow,.tips').removeClass('hide')

        //获取当前删除所在行的字段值
        var h_id = $(this).parent().parent().attr('hid')
        var node = $(this).parent().parent().attr('node')
        console.log("删除行id为:",h_id)
        console.log("删除行所属node为:",node)

        //将当前行id传递到弹出框中
        $('.tips').find('div[name="hid"]').val(h_id)
        $('.tips').find('div[name="node"]').val(node)
    })

    //环境、数据库详细信息删除取消
    $('#delEnvDetailCancelBtn').click(function () {
        $('.shadow,.tips').addClass('hide')
    })

    //环境、数据库详细信息删除确定
    $('#delEnvDetailConfirmBtn').click(function(){
        $.ajax({
            url:'/envManage/env/detail/del',
            type:'POST',
            data:{'hid':$('.tips_footer').val(),'node':$('#node_v').val()},
            dataType:'JSON',
            success:function (data) {
                console.log("后端返回数据：",data)
                if(data.status == 0){
                    location.reload()
                }else {
                    var error_obj = JSON.stringify(data.err_msg)  //转为字符串
                    console.log('error_obj:',error_obj,typeof(error_obj))
                    $.each($.parseJSON(error_obj),function(k,v){  //后端传过来是json对象，前端需要转为js对象，需要做个转换JSON.parse() 或者 jQuery $.parseJSON()
                        console.log('#####',k,v)
                        // 如果前端值在后端处理有问题，那么通过弹出框显示错误信息
                        $('.verfity_div').removeClass('hide')
                        $('#verfityInfo').text(v)
                        // 弹出框提示3秒后消失
                        setTimeout(function (){$('.verfity_div').addClass('hide')},3000 )
                        })
                }
            }
        })
    })

/*--------------添加操作--------------------*/
    //添加环境详细信息按钮
    $('#addEnvDetailBtn').click(function () {
        $('.shadow,.add_env_div').removeClass('hide')
    })

    //添加数据库详细信息按钮
    $('#addDbDetailBtn').click(function () {
        $('.shadow,.add_db_div').removeClass('hide')
    })

    //添加环境详细信息界面取消按钮
    $('#addEnvCancelBtn').click(function () {
        $('.shadow,.add_env_div').addClass('hide')
    })

    //添加数据库信息界面取消按钮
    $('#addDbCancelBtn').click(function () {
        $('.shadow,.add_db_div').addClass('hide')
    })

    //添加环境信息确定按钮
    $('#addEnvConfirmBtn').click(function(){
        $.ajax({
            url:'/envManage/env/detail/add',
            type:'POST',
            data:$('#addEnvForm').serialize(),
            dataType:'JSON',
            success:function (data) {
                console.log(data,typeof(data))
                if(data.status == 0){
                    location.reload()
                }else {
                    var error_obj = JSON.stringify(data.err_msg)  //转为字符串
                    console.log('error_obj:',error_obj,typeof(error_obj))
                    $.each($.parseJSON(error_obj),function(k,v){  //后端传过来是json对象，前端需要转为js对象，需要做个转换JSON.parse() 或者 jQuery $.parseJSON()
                        console.log('#####',k,v)
                        // 如果前端值在后端处理有问题，那么通过弹出框显示错误信息
                        $('.verfity_div').removeClass('hide')
                        $('#verfityInfo').text(v)
                        // 弹出框提示3秒后消失
                        setTimeout(function (){$('.verfity_div').addClass('hide')},3000 )
                        }
                    )
                }
            }
        })
    })

    //添加数据库信息确定按钮
    $('#addDbConfirmBtn').click(function(){
        $.ajax({
            url:'/envManage/db/detail/add',
            type:'POST',
            data:$('#addDbForm').serialize(),
            dataType:'JSON',
            success:function (data) {
                console.log(data,typeof(data))
                if(data.status == 0){
                    location.reload()
                }else {
                    var error_obj = JSON.stringify(data.err_msg)  //转为字符串
                    console.log('error_obj:',error_obj,typeof(error_obj))
                    $.each($.parseJSON(error_obj),function(k,v){  //后端传过来是json对象，前端需要转为js对象，需要做个转换JSON.parse() 或者 jQuery $.parseJSON()
                        console.log('#####',k,v)
                        // 如果前端值在后端处理有问题，那么通过弹出框显示错误信息
                        $('.verfity_div').removeClass('hide')
                        $('#verfityInfo').text(v)
                        // 弹出框提示3秒后消失
                        setTimeout(function (){$('.verfity_div').addClass('hide')},3000 )
                        }
                    )
                }
            }
        })
    })
}

