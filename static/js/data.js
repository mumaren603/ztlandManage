  //查询结果弹出框关闭 并清空页面数据
        $('#closeBtn').click(function(){
            $('#bdcdyh').html()
            $('#zddmOrFwdm').html()
            $('#bdcqzsOrZm').html()
            $('#tdOrFwzl').html()
            $('#resTab').addClass('hide')
        })

        // 查询
        $('#queryBtn').click(function () {

            //将查询按钮置为不可编辑且背景色置灰色
            $('#queryBtn').attr("disabled",true);
            $('#queryBtn').attr("class","queryBtn2");

            //获取页面请求值
            var env = $('#queryForm').find('select[name="env"]').val()
            var cq = $('input[type="radio"][name="cqmc"]:checked').val()
            var djlx = $('input[type="radio"][name="djlx"]:checked').val()
            // 获取复选框chekbox多个值
            var xzxx = []
            $('input[type="checkbox"][name="xzxx"]:checked').each(
                function () {
                    xzxx.push($(this).val())
                }
            )
            var sfpl = $('input[type="radio"][name="sfpl"]:checked').val()
            console.log("请求参数:env:%s cq:%s djlx:%s xzxx:%s sfpl:%s" ,env,cq,djlx,xzxx,sfpl)

            if ((env == undefined || env == '' || env == null) && (cq == undefined || cq == '' || cq == null) && (djlx == undefined || djlx == '' || djlx == null) && (sfpl == undefined || sfpl == '' || sfpl == null)) {
                // 查不到数据界面提示
                $('.verfity_div').removeClass('hide')
                $('#verfityInfo').text('请选择必填条件！')
                // 弹出框提示3秒后消失
                setTimeout(function () {
                    $('.verfity_div').addClass('hide')
                }, 3000)
                $('#texts').html("")
            } else {
                $.ajax({
                    url: '/dataManage/data',
                    type: 'POST',
                    data: $('#queryForm').serialize(),
                    dataType: 'JSON',
                    success: function (obj) {
                        console.log('后端返回数据：', obj)
                        if (obj){
                            //后端有返回则将查询按钮置为可编辑且背景色置蓝色
                            $('#queryBtn').attr("disabled",false);
                            $('#queryBtn').attr("class","queryBtn");

                            if (obj.status == 1) {
                                if (obj.data != 'null'){
                                    // 接口返回异常
                                    $('.verfity_div').removeClass('hide')
                                    $('#verfityInfo').text(obj.err_msg)
                                    // 弹出框提示3秒后消失
                                    setTimeout(function () {
                                        $('.verfity_div').addClass('hide')
                                    }, 3000)
                                    $('#texts').html("")
                                }
                                else{
                                    // 无数据返回
                                    $('.verfity_div').removeClass('hide')
                                    $('#verfityInfo').text(obj.err_msg)
                                    // 弹出框提示3秒后消失
                                    setTimeout(function () {
                                        $('.verfity_div').addClass('hide')
                                    }, 3000)
                                    $('#texts').html("")
                                }
                            } else {
                                bdcdyh = obj['data'][0]
                                zddmOrFwdm = obj['data'][1]
                                tdOrFwzl = obj['data'][2]
                                cqzsOrZm = obj['data'][3]
                                $('#bdcdyh').html(bdcdyh)
                                $('#zddmOrFwdm').html(zddmOrFwdm)
                                $('#bdcqzsOrZm').html(cqzsOrZm)
                                $('#tdOrFwzl').html(tdOrFwzl)
                                // 弹出框
                                $('#resTab').removeClass('hide')
                            }
                        }
                    }
                })
            }
        })