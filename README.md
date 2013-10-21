# Bits and Bobs
You've built a webapp, wonderful. Too bad there's a lot of holes. Here's what we're going to cover.

* CSS
* Static files
* Light styling
* `Url_for`
* Login
* Form verification
* Message flashing

## CSS Frameworks
Okay, looks like crap, let's fix it. Note all the weird classes on everything.

Add on the line immediately after the `<title>` tag on line 3,

    <link href="/static/css/bootstrap.css" rel="stylesheet">

Bam it's way better.

## Static

We'll add another css file. where does it go? Into the static/css folder. It's super spesh. Make a new file, main.css and add the following line:

    h2 {
        color: red;
    }

Add a link to your new stylesheet as in section 1. Reload, if h2 is red, you're good to go.

## Some light styling

Declare some things: (stage1)

## Url For

## Logins


Don't store _everything_ in a session. Hold one, maybe two things _at the most_. Just enough to grab more information as you need it.

## Your mission

There's a database provided for you, thewall.db, with the following schema

    users:
    id - int, primary key
    username - varchar
    password - varchar

    wall_posts:
    id - int, primary key
    owner_id - int (refers to users.id)
    author_id - int (refers to users.id)
    created_at - datetime
    content - text

You're going to build a 'wall' (think The Book of Faces), which will require the following handlers:

1.  A GET handler named `view_user`, with a url pattern of either:

    `/user/<username>` [(documentation here)](http://flask.pocoo.org/docs/quickstart/#variable-rules)

    The handler should take the username passed to it, look up that user's wall_posts in  order by id, then send the collection of rows to a template named wall.html.

    The wall template should use a {% for %} directive to loop through all the wall_post rows, and display them each in their own div, along with the author's name and the created_at time (formatted however you like).

    The template should also check if the browser is logged in using an {% if %} directive. If so, display a form whose method is POST and action is the url for handler number two. It should have only two input elements, a textarea and a submit button.,

2.  A POST handler named `post_to_wall`, with the _exact_ same pattern as the GET handler, which will do the following things:
    
    It will receive the text from handler number one, extract a username from the url, and extract the user id of the currently logged-in user from the session.

    It will search the users database table to find the user id associated with the username.

    It will insert a new row into the users database with the `owner_id` being the `user_id` associated with the username, and the author_id being that of the currently logged-in user.

    It will redirect _back_ to handler number one.

3.  A handler named `register` (provided for you, you just need to add one thing.

    You only need to add one thing here, check if the user is logged in. If so, redirect them to their own wall using `url_for`.
