/** cms_posts.py by Anderson Huang at 2019/1/10 16:51 **/

// 加精帖子功能
$(function () {
    $('.highlight-btn').click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr('data-id');
        var highlight = parseInt(tr.attr('data-highlight'));
        var url = "";
        if (highlight) {
            url = '/cms/uhpost/';
        } else {
            url = '/cms/hpost/';
        }
        zlajax.post({
            'url': url,
            'data': {
                'post_id': post_id
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    if (highlight) {
                        zlalert.alertSuccessToast('取消帖子加精成功！')
                    } else {
                        zlalert.alertSuccessToast('帖子加精成功！')
                    }
                    setTimeout(function () {
                        window.location.reload();
                    }, 500);
                } else {
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});


// 后台移除帖子功能
$(function () {
   $('.delete-post-btn') .click(function (event) {
       event.preventDefault();

       var self = $(this);
       var tr = self.parent().parent();
       var post_id = tr.attr('data-id');

       zlalert.alertConfirm({
            'msg': "您确定要删除这个帖子吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dpost/',
                    'data': {
                        'post_id': post_id,
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.reload();
                        } else {
                            zlalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
   });
});
