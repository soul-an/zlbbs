/** boards.py by Anderson Huang at 2019/1/7 16:16 **/

// 添加板块
$(function () {
    $('#add-board-btn').click(function (event) {
        event.preventDefault();

        zlalert.alertOneInput({
            'text': '请输入板块名称！',
            'placeholder': '板块名称',
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    'url': '/cms/aboard/',
                    'data': {
                        'name': inputValue
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


// 更新板块
$(function () {
    $('.edit-board-btn').click(function (event) {
        event.preventDefault();

        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var board_id = tr.attr('data-id');

        zlalert.alertOneInput({
            'text': '请输入新的板块名称！',
            'placeholder': name,
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    'url': '/cms/uboard/',
                    'data': {
                        'board_id': board_id,
                        'name': inputValue
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

// 删除板块
$(function () {
    $(".delete-board-btn").click(function (event) {
        event.preventDefault();

        var self = $(this);
        var tr = self.parent().parent();
        var board_id = tr.attr('data-id');

        zlalert.alertConfirm({
            'msg': "您确定要删除这个板块吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dboard/',
                    'data': {
                        'board_id': board_id
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


