/** resetpwd.py by Anderson Huang at 2018/12/26 10:35 **/

$(function () {
    $("#submit").click(function (event) {
        // 阻止按钮默认提交表单的事件
        event.preventDefault();

        // 获取输入值
        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        // AJAX处理CSRF漏洞步骤：
        // 1. 要在模板meta标签中渲染一个csrf_token()
        // 2. 在ajax请求的头部中设置X-CSRFtoken
        zlajax.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data) {
                // console.log(data);
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast("恭喜！密码修改成功！");
                    // 清除输入框中的内容
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwd2E.val("");
                } else {
                    var message = data['message'];
                    zlalert.alertInfo(message)
                }
            },
            'fail': function (error) {
                // console.log(error);
                zlalert.alertNetworkError();
            }
        });
    });
});
