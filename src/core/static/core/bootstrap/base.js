$(document).ready(function () {

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $('meta[name=csrf]').attr("content"));
            }
        }
    });

    function updateLikes() {
        var posts = Array()
        var url = null

        $('.likecount').each(function () {
            posts.push($(this).data('postid'));
            url = $(this).data('url-count');
        })
        if (url != null) {
            $.getJSON(url, {posts: posts.join(',')}, function (data) {
                for (var i in data) {
                    $('.likecount[data-postid=' + i + ']').html(data[i]);
                }
            })
        }
    }

    function updateComment() {

        $('.comments_div').load($('.comments_div').data('url'))
    }

    window.setInterval(updateLikes, 1000)
    window.setInterval(updateComment, 2000)

    $('.autoload').each(function () {
        $(this).load($(this).data('url'));
    });

    $('.dialog-link').click(function () {
        $('#exampleModal').modal();
        $('.modal-body').load($(this).attr('href'));
        return false
    });

    $(document).on('submit', '.ajax-form', function () {
        var form = $(this);
        $.post(form.attr('action'), form.serialize(), function (data) {
            if (data == 'OK') {
                location.reload();
            }
            else {
                form.html(data)
            }
        });
        return false;
    });

    $(document).on('submit', '.registration-form', function () {
        var form = $(this);
        $.ajax({
            url: $(this).attr('action'),
            type: "POST",
            data: new FormData(this),
            contentType: false,
            cache: false,
            processData: false,
        }).done(function (data, status, response) {
            if (data == 'OK') {
                location.reload();
            }
            else {
                form.html(data);
            }
        });
        return false;
    });

     $(function() {
        $('.chosen-select').chosen();
        $('.chosen-select-deselect').chosen({ allow_single_deselect: true });
      });

    $(document).on('click', 'button.ajaxlike', function (e) {
        var data = $(this).data();
        var but = $(this)
        $.ajax({url: data.url, method: 'post'}).done(function (data, status, response) {
            but.html(data);
        })
        return false;
    });

});
