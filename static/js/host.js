    // 查询
    $('#queryBtn').click(function () {
            var  intranetIP = $('#queryForm').find('input[name="intranetIP"]').val()
            var  extrantIP = $('#queryForm').find('input[name="extrantIP"]').val()
            var  serverType = $('#queryForm').find('select[name="serverType"]').val()
            var  serverOs = $('#queryForm').find('select[name="serverOs"]').val()
            if ((intranetIP == undefined || intranetIP == '' || intranetIP == null) && (extrantIP == undefined || extrantIP == '' || extrantIP == null) && (serverType == undefined || serverType == '' || serverType == null) && (serverOs == undefined || serverOs == '' || serverOs == null)){
                debugger
                // 查不到数据界面提示
                $('.verfity_div').removeClass('hide')
                $('#verfityInfo').text('请至少输入一个查询条件！')
                // 弹出框提示3秒后消失
                setTimeout(function (){$('.verfity_div').addClass('hide')},3000 )
                $('#texts').html("")
            }

            else{
                debugger
                $.ajax({
                    url:'/hostManage/host',
                    type:'POST',
                    data:$('#queryForm').serialize(),
                    dataType:'JSON',
                    success:function (data) {
                        debugger
                        console.log('data',data)
                        if (data == null || data == '')
                        {
                            // 查不到数据界面提示
                            $('.verfity_div').removeClass('hide')
                            $('#verfityInfo').text('没有查询到数据！')
                            // 弹出框提示3秒后消失
                            setTimeout(function (){$('.verfity_div').addClass('hide')},3000 )
                            $('#texts').html("")
                        }else{
                            var html = ""
                            for(var i=0;i < data.length;i++){
                                html += '<tr><td>' + (Number(i)+Number('1') )+ '</td>' +
                                    '<td>' + data[i].intranetIP + '</td>' +
                                    '<td>' + data[i].extrantIP + '</td>' +
                                    '<td>' + data[i].serverType + '</td>' +
                                    '<td>' + data[i].serverPurpose + '</td>' +
                                    '<td>' + data[i].serverOs + '</td>' +
                                    '<td>' + data[i].serverAccount + '</td>' +
                                    '<td>' + data[i].serverPassword + '</td>' +
                                    '<td>' + data[i].originServer + '</td>' +
                                    '<td><input class="edit_host_btn" type="button" value="编辑">'+
                                    '<input class="del_host_btn" type="button" value="删除"></td></tr>'
                            }
                            $('#texts').html(html)
                        }
                    }
                })
            }
            })

    //编辑
    $('.edit_host_btn').click(function () {
        debugger
        console.log('编辑。。。')
        $('.shadow,.edit_div').removeClass('hide')

        //获取当前编辑所在行的字段值
        var h_id = $(this).parent().parent().attr('hid')
        var frontIP = $(this).parent().parent().children('td[name="frontIP"]').text()
        var backIP = $(this).parent().parent().children('td[name="backIP"]').text()
        var dbIP = $(this).parent().parent().children('td[name="dbIP"]').text()
        var env_name = $(this).parent().parent().children('td[name="env_name"]').text()
        var status = $(this).parent().parent().children('td[name="status"]').text()

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
    $('#edit_confirm_btn').click(function(){
        $.ajax({
            url:'/envManage/env/edit',
            type:'POST',
            data:$('#edit_form').serialize(),
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

    //删除
    $('.del_env_btn').click(function () {
        $('.shadow,.tips').removeClass('hide')

        //获取当前删除所在行的字段值
        var h_id = $(this).parent().parent().attr('hid')
        console.log("环境主信息删除行id为:",h_id)

        //将当前行id传递到弹出框中
        $('.tips').find('div[name="hid"]').val(h_id)
    })

    //删除取消
    $('#delEnvCancelBtn').click(function () {
        $('.shadow,.tips').addClass('hide')
    })

    //删除确定
    $('#delEnvConfirmBtn').click(function(){
        $.ajax({
            url:'/envManage/env/del',
            type:'POST',
            data:{'hid':$('.tips_footer').val()},
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