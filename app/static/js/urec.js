/**
 * Created by leo on 17-4-19.
 */
function display_in_div(div, contents) {
    console.log(contents);
    var inner = '<h1 class="text-primary page-header">为你推荐</h1>';
    for (var i = 0; i < contents.length; i++) {
        if (i % 4 == 0) {
            inner += '<div class="row">'
        }
        inner += `<div class="col-sm-4 col-md-3 center">
                    <img src="` + contents[i].poster + `" class="img-rounded" width="120px"><br/>
                    <a href="/lens2mid/`+ contents[i].mid + `" class="text-primary">` + contents[i].title + `</a>
                    <h5 class="text-danger">` + contents[i].rating + `</h5>
                    <a href="/lens2mid/`+ contents[i].mid + `" class="text-warning">` + contents[i].mid + `</a>
                </div>`;
        if (i % 4 == 3) {
            inner += '</div><br/>'
        }
    }
    div.html(inner)
}

$(function () {
    var div = $("#rec");

    $.ajax("/api/cf/", {
        method: 'GET',
        data: {
            uid: $("#hidden_uid").text(),
            n: 16
        }
    }).done(function (data) {
        var json = $.parseJSON(data);
        console.log(json.status);
        if (json.status == 200) {
            var contents = json.contents;
            display_in_div(div, contents)
        }
    }).fail(function (xhr, status) {
        console.log(xhr.status);
        console.log(status)
    });
});



