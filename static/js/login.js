    //登录
    $('#loginBtn').click(function () {
        $.ajax({
            url:'/login/',
            method:'POST',
            data:$('#login-form').serialize(),
            dataType:'JSON',
            success:function (data) {
                console.log(data,typeof(data))
                if(data.status == 0){
                    window.location.href="/env"
                }else {
                    var errMsg = data.err_msg
                    console.log('errMsg',errMsg)
                    $('.shadow').removeClass('hide')
                    $('.tips').removeClass('hide')
                    $('.tips_body').html(errMsg)
                }
            }
        })
    })

    //登录弹出框关闭按钮
    $('#loginErrTipsBtn').click(function () {
        $('.shadow').addClass('hide')
        $('.tips').addClass('hide')
    })