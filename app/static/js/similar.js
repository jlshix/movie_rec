/**
 * Created by leo on 17-4-19.
 */
function display_in_div(div, contents) {
    console.log(contents);
    var inner = '<h1 class="text-primary page-header">相似电影</h1>';
    for (var i = 0; i < contents.length; i++) {
        if (i % 4 == 0) {
            inner += '<div class="row">'
        }
        inner += `<div class="col-sm-4 col-md-3 center">
                    <img src="` + contents[i].poster + `" class="img-rounded" width="120px">
                    <h5 class="text-primary">` + contents[i].title + `</h5>
                    <h5 class="text-primary">` + contents[i]._id + `</h5>
                </div>`;
        if (i % 4 == 3) {
            inner += '</div><br/>'
        }
    }
    div.html(inner)
}

$(function () {
    var div = $("#rec");

    $.ajax("/api/rec/sum/", {
        method: 'GET',
        data: {
            id: document.URL.split('/')[4],
            limit: 16,
            skip: 0
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



