/** front_signup.py by Anderson Huang at 2019/1/1 18:18 **/

$(function () {
    $('#captcha-img').click(function (event) {
        var self = $(this)
        var src = self.attr('src');
        var newsrc = zlparam.setParam(src, 'xx', Math.random());

        self.attr('src', newsrc);
    });
});
