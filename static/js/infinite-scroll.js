let page = 1;
let isLoading = false;

function loadMorePosts() {
    if(isLoading) return;
    isLoading = true;
    $.ajax({
        url: '/load-more-posts/' + page,
        type: 'GET',
        success: function(posts) {
            if (posts.length === 0) {
                $('#loader').hide();
                isLoading = false;
                return;
            }
            posts.forEach(function(post) {
                $('#content').append(
                    '<div class="posts">' +
                    '<img src="' + post.image_url + '" alt="' + post.title + '">' +
                    '<h2>' + post.title + '</h2>' +
                    '<p>' + post.content + '</p>' +
                    '</div>'
                );
            });
            page++;
            isLoading = false;
        },
        error: function(xhr, status, error) {
            console.error("An error occurred when loading more posts: ", status, error);
            isLoading = false;
        }
    });
}

$(window).scroll(function() {
    if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
        loadMorePosts();
    }
});