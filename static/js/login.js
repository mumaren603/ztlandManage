    //登录
    $('#loginBtn').click(function () {
        debugger
        var username_v = $('#login-form').find('input[name="username"]').val()
        console.log('用户名',username_v)
        var password_v = $('#login-form').find('input[name="password"]').val()
        console.log('密码',password_v)

        if(username_v && password_v){
            debugger
            $.ajax({
            url:'/common/login',
            method:'POST',
            data:$('#login-form').serialize(),
            dataType:'JSON',
            success:function (data) {
                debugger
                console.log(data,typeof(data))
                if(data.status == 0){
                    debugger
                    console.log("登录成功，正在跳转到env.html页面")
                    window.location.href="/envManage/env"
                }else {
                    debugger
                    var errMsg = data.err_msg
                    console.log('errMsg',errMsg)
                    $('.shadow').removeClass('hide')
                    $('.tips').removeClass('hide')
                    $('.tips_body').html(errMsg)
                }
            }
        })
        }else{
            debugger
            var errMsg = '用户名和密码不可为空！'
            console.log('errMsg',errMsg)
            $('.shadow').removeClass('hide')
            $('.tips').removeClass('hide')
            $('.tips_body').html(errMsg)
        }

    })

    //登录弹出框关闭按钮
    $('#loginErrTipsBtn').click(function () {
        $('.shadow').addClass('hide')
        $('.tips').addClass('hide')
    })