/** resetemail.py by Anderson Huang at 2018/12/27 14:52 **/

// 前端修改邮箱发送验证码
$(function () {
    $('#captcha-btn').click(function (event) {
        event.preventDefault();

        var email = $("input[name='email']").val()
        if (!email) {
            zlalert.alertInfoToast('请输入新的邮箱！');
            return;
        }
        zlajax.get({
            'url': '/cms/email_captcha/',
            'data': {
                'email': email
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast('邮件验证码发送成功！');
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});

// 前端修改邮箱验证
$(function () {
    $('#submit').click(function (envent) {
        event.preventDefault();

        var emailE = $("input[name='email']");
        var captchaE = $("input[name='captcha']");

        var email = emailE.val();
        var captcha = captchaE.val();

        zlajax.post({
            'url': '/cms/resetemail/',
            'data': {
                'email': email,
                'captcha': captcha
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    emailE.val("");
                    captchaE.val("");
                    zlalert.alertSuccessToast('恭喜！邮箱修改成功！');
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});
