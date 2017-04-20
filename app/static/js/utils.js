/**
 * Created by leo on 17-4-19.
 */

// 异步请求数据设定当前状态
$(function () {
    $.ajax("/api/movie/state", {
        method: 'GET',
        data: {
            id: document.URL.split('/')[4],
            uid: $('#uid').text()
        }
    }).done(function (data) {
        var json = $.parseJSON(data);
        console.log(json.status);
        if (json.status == 200) {
            json.res.want ? $("#want").text("已想看") : $("#want").text("想看");
            json.res.watching ? $("#watching").text("已在看") : $("#watching").text("在看");
            json.res.watched ? $("#watched").text("已看过") : $("#watched").text("看过");
            json.res.like ? $("#like").text("已喜欢") : $("#like").text("喜欢");
        }
    }).fail(function (xhr, status) {
        console.log(xhr.status);
        console.log(status)
    });
});


// 更改想看状态
$(function () {
    var a = $("#want");
    a.click(function () {
        if (a.text() == "想看") {
            $.ajax('/api/subject/25934014', {
                method: 'POST',
                data: {
                    id: document.URL.split('/')[4],
                    uid: $('#uid').text()
                }
            }).done(function (data) {
                var json = $.parseJSON(data);
                console.log(json.title);
            }).fail(function (xhr, status) {
                console.log(xhr.status);
                console.log(status)
            });
            a.text("已想看");
        } else if (a.text() == "已想看") {
            a.text("想看");
        } else {
            alert(a.text())
        }
    });

});