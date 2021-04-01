window.onload=function(){
    var auth = $('#addEnvInfo').attr('auth')
     console.log("当前登录人具有权限编码为：",auth,typeof(auth))

    //根据后端返回权限码判断当前用户是否有权限访问按钮（看见）
    var code ='env_add'
    if(auth.includes(code) || auth.includes('auth_all')){
        $('#addEnvInfo').attr("style","display:inline-block;")
    }

    //添加操作
    $('#addEnvInfo').click(function () {
        $('.shadow,.add_div').removeClass('hide')
    })

    //添加取消
    $('#add_cancel_btn').click(function () {
        $('.shadow,.add_div').addClass('hide')
    })

    //添加确定
    $('#add_confirm_btn').click(function(){
        $.ajax({
            url:'/env/addEnv',
            type:'POST',
            data:$('#add_form').serialize(),
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

}

