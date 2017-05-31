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
                    <img src="` + contents[i].poster + `" class="img-rounded" width="120px"><br/>
                    <a href="/subject/` + contents[i]._id + `" class="text-primary">` + contents[i].title + `</a>
                    <h5 class="text-danger">`+ contents[i].lens_id + '  ' + contents[i].rank +`</h5>
                    <a href="/subject/` + contents[i]._id + `" class="text-primary">` + contents[i]._id + `</a>
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
            limit: 17,
            skip: 1
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


