document.addEventListener('DOMContentLoaded', function() {
    //window.history.pushState('Network','Network','http://127.0.0.1:8000/')

    document.querySelector('#user-info').style.display = 'none';
    document.querySelector('#new-post').style.display = 'none';
    document.querySelector('#all-posts').style.display = 'block';
    
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
    document.querySelector('#new-post').style.display = 'none';
    document.querySelector('#all-posts').style.display = 'none';
    // Clear profile div
    document.querySelector('#user-info').innerHTML = ``;
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
        if (userdata.can_follow) {
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
        document.querySelector('#follow_button').addEventListener("click", () => follow_unfollow(userdata.user_id));
        // Display Your posts
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
    document.querySelector('#new-post').style.display = 'none';
    document.querySelector('#all-posts').style.display = 'block';

    document.querySelector('#all-posts').innerHTML = ``;
    document.querySelector('#user-info').innerHTML = ``;

    const h1 = document.createElement('h1')
    h1.innerHTML = 'All Posts'
    document.querySelector('#all-posts').append(h1);

    const allpostsdiv = document.createElement('div')
    allpostsdiv.id = 'user-posts'
    document.querySelector('#all-posts').append(allpostsdiv);

    show_all_posts();
}


function show_all_posts(){
    fetch('/allposts')
    .then(response => response.json())
    .then(allposts => show_posts(allposts))
}


function following_posts(){
    document.querySelector('#user-info').style.display = 'none';
    document.querySelector('#new-post').style.display = 'none';
    document.querySelector('#all-posts').style.display = 'block';

    document.querySelector('#all-posts').innerHTML = ``;
    document.querySelector('#user-info').innerHTML = ``;

    const h1 = document.createElement('h1')
    h1.innerHTML = 'People you follow wrote:'
    document.querySelector('#all-posts').append(h1);

    const followingposts = document.createElement('div')
    followingposts.id = 'user-posts'
    document.querySelector('#all-posts').append(followingposts);

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
        const likes = userpost.likes;
        const post = document.createElement('div')
        post.id = `post_${userpost.id}`
        post.className = 'single-post'
        post.innerHTML = '<p><strong><a href="#" onclick="profile('+ userpost.author_id + ')">' + userpost.author + '</a></strong></p> <p>' + userpost.content + '</p> <p class="small">' + userpost.date + '</p>' + '<p><a href="#"><i class="fa-heart fa-solid"></i></a> ' + likes + '</p>';
        document.querySelector('#user-posts').append(post); 
    });    
}


// Follow or unfollow
function follow_unfollow(user_id){
    profile(1);
}