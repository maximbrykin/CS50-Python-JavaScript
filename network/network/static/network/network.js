document.addEventListener('DOMContentLoaded', function() {
    //window.history.pushState('Network','Network','http://127.0.0.1:8000/')

    document.querySelector('#user-info').style.display = 'none';
    
    all_posts();
    //profile(1);

    // Menu clicks
    if (document.getElementById('profile')) {
        document.querySelector('#profile').addEventListener("click", (p) => profile(p.target.closest("#profile").dataset.user_id));    
    } 
    if (document.getElementById('following')) {
        document.querySelector('#following').addEventListener("click", () => following_posts());
    } 
    document.querySelector('#homepage').addEventListener("click", () => all_posts());

   
});


function profile(user_id){
    
    // Show profile div and hide other divs
    document.querySelector('#user-info').style.display = 'block';

    // Clear profile div
    document.querySelector('#user-info').innerHTML = ``;
    document.querySelector('#posts').innerHTML = ``;
    // Create profile structure
    const usernamediv = document.createElement('div');
    usernamediv.id = 'username';
    document.querySelector('#user-info').append(usernamediv);
    const userposts = document.createElement('div');
    userposts.id = 'user-posts';
    document.querySelector('#user-info').append(userposts);

    show_user_info(user_id);
    show_user_posts(user_id);
}


function show_user_info(user_id){
    
    fetch(`/profile/${user_id}`)
    .then(response => response.json())
    .then(userdata => {
        console.log(userdata);
        // Display Username
        const username = document.createElement('h1')
        username.innerHTML = userdata.username
        document.querySelector('#username').append(username)
        // Display Mood
        const userinfo = document.createElement('div')
        userinfo.id = 'mood'
        userinfo.innerHTML = '<i>(' + userdata.mood + ')</i>'
        document.querySelector('#username').append(userinfo); 
        // Display followers
        const following = document.createElement('div')
        following.id = 'followers'
        following.innerHTML = 'Following: ' + userdata.follows_num
        document.querySelector('#username').append(following)
        // Display followed
        const followed = document.createElement('div')
        followed.id = 'followed'
        followed.innerHTML = 'Followed by: ' + userdata.followed_by_num
        document.querySelector('#username').append(followed);
        // Display follow button
        const follow = document.createElement('button')
        follow.id = 'follow_button'
        follow.className = 'btn btn-light'
        if (userdata.can_be_followed) {
            follow.style.display = 'unset';
            if (userdata.is_following) {
                follow.innerHTML = 'Unfollow';
            } else {
                follow.innerHTML = 'Follow';
            }
        } else {
            follow.style.display = 'none';
        }
        document.querySelector('#username').append(follow);
        document.querySelector('#follow_button').addEventListener("click", () => follow_unfollow(user_id));
        // Display User's posts title
        const yourposts = document.createElement('h3')
        yourposts.innerHTML = '<br>' + userdata.username + '`s posts:'
        document.querySelector('#username').append(yourposts);            
    });
}
    

function show_user_posts(user_id){
    fetch(`/posts/${user_id}`)
    .then(response => response.json())
    .then(userposts => show_posts(userposts))
}


function all_posts(){
    document.querySelector('#user-info').style.display = 'none';

    document.querySelector('#posts').innerHTML = ``;

    const h1 = document.createElement('h1')
    h1.innerHTML = 'All Posts'
    document.querySelector('#posts').append(h1);

    const allpostsdiv = document.createElement('div')
    allpostsdiv.id = 'user-posts'
    document.querySelector('#posts').append(allpostsdiv);

    show_all_posts();
}


function show_all_posts(){
    fetch('/allposts')
    .then(response => response.json())
    .then(allposts => show_posts(allposts))
}


function following_posts(){
    document.querySelector('#posts').style.display = 'block';

    document.querySelector('#posts').innerHTML = ``;
    document.querySelector('#user-info').innerHTML = ``;


    const h1 = document.createElement('h1')
    h1.innerHTML = 'People you follow wrote:'
    document.querySelector('#posts').append(h1);

    const followingposts = document.createElement('div')
    followingposts.id = 'user-posts'
    document.querySelector('#posts').append(followingposts);

    show_following_posts();
}


function show_following_posts(){
    fetch('/following_posts')
    .then(response => response.json())
    .then(following => show_posts(following))
}


function show_posts(posts){
    //console.log(posts)
    // Display posts
    posts.forEach(userpost => {
        
        const post = document.createElement('div')
        post.id = `post_${userpost.id}`
        post.className = 'single-post'
        // Username row
        const username = document.createElement('div')
        username.id = `user`;
        username.innerHTML = '<p><strong><a href="#" onclick="profile('+ userpost.author_id + ')">' + userpost.author + '</a></strong></p>'
        post.append(username);
        // Content row
        const content = document.createElement('div')
        content.id = `content_${userpost.id}`;
        content.innerHTML = '<p>' + userpost.content + '</p>'
        post.append(content);
        // Date row
        const date = document.createElement('div')
        date.id = `date_${userpost.id}`;
        date.innerHTML = '<p class="small">' + userpost.date + '</p>';
        post.append(date);
        // Edit button
        if (userpost.can_edit) {
            const edit_btn = document.createElement('button');
            edit_btn.className ="btn btn-link edit_btn";
            edit_btn.innerHTML = "Edit";
            edit_btn.id = `edit_btn_${userpost.id}`
            edit_btn.addEventListener('click', () => edit_post(userpost));
            post.append(edit_btn);
        }
        // Like row
        const likes_row = document.createElement('div')
        likes_row.id = `likes_${userpost.id}`;
        // Like icon
        const like_icon = document.createElement('i');
        like_icon.id = `like_icon_${userpost.id}`;
        let icon_bg;
        if (userpost.liked_by){
            icon_bg = 'fa-solid';
        } else {
            icon_bg = 'fa-regular';
        }
        like_icon.className = `like-icon fa-heart ${icon_bg}`;
        if (document.getElementById('profile')) {
            like_icon.addEventListener('click', () => set_like(userpost));
        } else {
            like_icon.addEventListener('click', () => go_login());
        }
        // Likes number
        const likes = userpost.likes;
        const like_num = document.createElement('p');
        like_num.id = `like_num_${userpost.id}`;
        like_num.className = 'like-num';
        like_num.innerHTML = likes;
        // Combine Divs for a like row
        likes_row.append(like_icon);
        likes_row.append(like_num);
        post.append(likes_row);

        document.querySelector('#user-posts').append(post);
    });    
}


function edit_post(post){
    const content = document.getElementById(`content_${post.id}`);
    const likes = document.getElementById(`likes_${post.id}`);
    const date = document.getElementById(`date_${post.id}`);
    const edit_btn = document.getElementById(`edit_btn_${post.id}`);
    const post_body = content.parentNode;
    
    
    // Edit buttons
    const edit_btns = document.createElement('div');
    //Save button
    const save_button = document.createElement('button');
    save_button.className = "btn btn-success";
    save_button.type = "button";
    save_button.innerHTML = "Save";
    save_button.addEventListener('click', () => {
        const new_content = document.getElementById(`new_content_${post.id}`).value;
        /*body = JSON.stringify({
            post_id: post.id,
            new_content: new_content});
        console.log(body);*/
        fetch(`/save_post`, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': getCookie("csrftoken")
            },
            body: body = JSON.stringify({
                post_id: post.id,
                new_content: new_content,
            })
        })
        .then(response => response.json())
        .then(response => {
            if (response.result) {
                content.innerHTML = new_content;
            } else {
                alert("Cannot edit this post.");
            }
            edit_btns.remove();
            content_editable.remove();
            post_body.append(content);
            post_body.append(date);
            post_body.append(edit_btn);
            post_body.append(likes);
        });
    });

    const content_editable = document.createElement('input');
    content_editable.id = `new_content_${post.id}`;
    content_editable.type = "textarea";
    content_editable.className = "form-control";
    content_editable.value = content.innerHTML;

    document.getElementById(`content_${post.id}`).remove();
    document.getElementById(`date_${post.id}`).remove();
    document.getElementById(`edit_btn_${post.id}`).remove();
    document.getElementById(`likes_${post.id}`).remove();
    

    edit_btns.append(content_editable);
    edit_btns.append(save_button);

    // Cancel button
    const cancel_btn = document.createElement('button');
    cancel_btn.type = "button";
    cancel_btn.className = "btn btn-danger";
    cancel_btn.innerHTML = "Cancel";
    cancel_btn.addEventListener('click', () => {
        edit_btns.remove();
        content_editable.remove();
        post_body.append(content);
        post_body.append(date);
        post_body.append(edit_btn);
        post_body.append(likes);
    });
    edit_btns.append(cancel_btn);
    post_body.appendChild(edit_btns);
}

function set_like(post){
    fetch(`/post/${post.id}/set_like`)
    .then(response => response.json())
    .then(response => {
        if (response.liked) {
            document.getElementById(`like_icon_${post.id}`).className = 'like-icon fa-heart fa-solid';
        } else {
            document.getElementById(`like_icon_${post.id}`).className = 'like-icon fa-heart fa-regular';
        }
        document.getElementById(`like_num_${post.id}`).innerHTML = response.new_like_num;
    })
}

// Follow or unfollow
function follow_unfollow(user_id){
    fetch(`/profile/${user_id}/follow`)
    .then(response => response.json())
    .then(response => {
        if (response.following) {
            document.getElementById('follow_button').innerHTML = 'Unfollow';
        } else {
            document.getElementById('follow_button').innerHTML = 'Follow';
        }
        document.getElementById('followed').innerHTML = 'Followed by: ' + response.new_followers_num;
    })
}


function go_login(){
    window.location = '/login';
}


function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}