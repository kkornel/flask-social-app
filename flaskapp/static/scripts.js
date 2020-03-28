var form = document.forms.namedItem("formData");
form.addEventListener('submit', function (ev) {
    var oData = new FormData(form);
    //for (var p of oData) {
    //    console.log(p);
    //}
    $.ajax({
        url: '/post-create-modal/',
        type: 'POST',
        method: 'POST',
        data: oData,
        enctype: 'multipart/form-data',
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            console.log(data);
            $('#postCreateModal').modal('hide');
            // If false, the page will be reloaded from cache, 
            // if true, from the server,
            // default value is false.
            window.location.reload(true);
        },
        error: function (data) {
            console.log(data);
            $('#postCreateModal').modal('hide');
            window.location.reload(true);
        },
    });
    ev.preventDefault();
}, false);

function send_like(event, post_id, profile_id, a_id) {
    const aHrefLike = $('#' + a_id);
    const isLiked = aHrefLike.hasClass('liked');
    const smallTextLikesCount = $('#' + a_id).find("#post-likes-count");
    aHrefLike.toggleClass("liked");
    aHrefLike.toggleClass("heart");
    $.ajax({
        url: '/like/',
        type: 'POST',
        data: {
            'post_id': post_id,
            'profile_id': profile_id,
        },
        success: function (data) {
            let likesCount = parseInt(data.likes_count);
            smallTextLikesCount.text(likesCount);
        },
        error: function (data) {
            console.log(data);
        },
    });
    event.stopImmediatePropagation();
}

function follow_user(event, follower_id, followed_id, is_from_modal, a_id) {
    const aHrefFollow = $('#' + a_id);
    if (is_from_modal) {
        aHrefFollow.toggleClass("purple-btn-outline-modal");
    } else {
        aHrefFollow.toggleClass("purple-btn-outline");
    }
    aHrefFollow.toggleClass("purple-btn");
    aHrefFollow.text((aHrefFollow.text() == 'Follow') ? 'Following' : 'Follow');
    $.ajax({
        url: '/follow/',
        type: 'POST',
        data: {
            'follower_id': follower_id,
            'followed_id': followed_id,
        },
        success: function (data) {
            if (is_from_modal) {
                return
            }
            console.log(data);
            followers = data.followers
            following = data.following
            $('#followers-count').text(followers);
            $('#following-count').text(following);
        },
        error: function (data) {
            console.log(data);
        },
    });
    event.stopImmediatePropagation();
}

function delete_comment_or_post(that, event, what_to_delete) {
    console.log(what_to_delete);
    let title = '';
    let content = '';
    if (what_to_delete == 'post') {
        title = 'Delete post';
        content = 'Are you sure you want to delete this post?';
    } else if (what_to_delete == 'comment') {
        title = 'Delete comment';
        content = 'Are you sure you want to delete this comment?';
    }
    var object_to_delete_id = $(that).data('id');
    console.log(object_to_delete_id)
    $('#modalDeleteTitle').text(title);
    $('#modalDeleteContent').text(content);
    $('#deletePostModal').modal('show');
    $(".modal-body #objtectToDeleteId").val(what_to_delete + '-' + object_to_delete_id);
    stopPropagation(event);
};

function send_request_to_delete_object() {
    var object_to_delete_id = $(".modal-body #objtectToDeleteId").val();
    console.log(object_to_delete_id);

    $.ajax({
        url: '/delete_comment_or_post/',
        type: 'POST',
        data: {
            'object_to_delete_id': object_to_delete_id,
        },
        success: function (data) {
            console.log(data);
            $('#deletePostModal').modal('hide');
            window.location.reload();
        },
        error: function (data) {
            console.log(data);
            $('#deletePostModal').modal('hide');
            window.location.reload();
        },
    });
};

function openInNewTab(event, url) {
    var win = window.open(url, '_blank');
    win.focus();
    event.stopImmediatePropagation();
}

$('.dropdown-arrow').click(function (event) {
    // It solves problem of not opening the dropdown at first click.
    event.stopPropagation();
});

function stopPropagationForGivenPost(event, postId) {
    // It's used to show dropdown without trigerring 
    // onlick of whole post.
    $('#' + postId).dropdown();
    event.stopPropagation();
}

function stopPropagation(event) {
    event.stopPropagation();
}

function stopImmediatePropagation(event) {
    event.stopImmediatePropagation();
}