# Bits and Bobs
You've built a webapp, wonderful. It works, and not too shabbily. But there are a lot of quality-of-life-items which would be nice to add that make our lives much easier, and our app much smoother. We'll add them here. We'll be covering the following things:

* CSS frameworks
* Static files
* Light styling
* Template inheritance
* URL Management
* Sessions
* Message flashing

## Taking Stock
First thing's first, clone this repository, create a new virtual environment, and reconstruct the required packages.

    $ virtualenv --clear --no-site-packages env
    $ source env/bin/activate
    $ pip install -r requirements.txt

Start the app by running app.py, open the same file in sublime, then browse over to [http://localhost:5000](localhost) and let's see what we've got.

So far, we have a crummy login page. We also have three handlers, two of which use the same url, we'll cover that in a second. We also have a model file, which has one function, authenticate, and information for an ADMIN user of sorts. Let's start by fixing this login page.

## CSS Frameworks
Looking at the `index` handler, we can see that it renders the index.html template. Open that in your editor.

Man, that's just hideous in the browser, but the html itself is structurally sound. It's very basic, too. Just a form with some inputs and a button, and some divs for separation. Note all the odd classes on the elements. Other than that, normal html. Now for the fun.

Add on the line immediately after the `<title>` tag on line 3,

    <link href="/static/css/bootstrap.css" rel="stylesheet">

Bam. It's way better. Welcome to [http://getbootstrap.com/getting-started/#template](Bootstrap).

In short, bootstrap is a series of CSS design decisions made for you. It's pretty great, because it takes away a lot of the 'hideous' factor. The only thing you need to do is organize your divs according to how they want you to, and give them the right class names. This is fine, because all things considered, bootstrap has some pretty good names and pretty good nesting conventions. Play by their rules, and everything looks amazing.

However, since _everyone_ is using bootstrap, every website ever looks amazing in exactly the same way. They're like the Stepford Wives of web programming.

## Static
So we used kind of an unusual url for our bootstrap file. It starts with '/static'. This folder is super spesh. Normally, our urls aren't really files, they map to functions instead. This becomes problematic when we want to actually point to a real file. When we _do_ point to real files, they're usually files that don't change, like images or css. They're static files (as opposed to our templates, which are mad-libbed on the fly, and thus dynamic). We have a place to put these files, the eponymously-named static folder. It's here you'll put your files which remain the same throughout eternity, slowly gathering dust as the ages pass.

Where were we.

Right. Static. We'll add another css file. Where does it go? Into the static/css folder. Name it main.css, and fill it with the following:

    h2 {
        color: red;
    }

Any file in the static folder will start with the url '/static'. That leading slash is important, don't forget it. You'll be sad if you do. It'll be sad if you forget it, too. It thought you were friends.

Add a link to your new stylesheet as we did in the bootstrap section. Don't replace bootstrap, just add it _afterwards_. Reload the page and your form header should now be red. If it is, you're good to go. Remove that red styling and proceed.

## Some light styling
We're gonna give our app a little updo. First, this background's too bright. It hurts my eyes. Add this style to main.css, always reloading and checking your work:

    body {
        background-color: #eee;
    }

A lovely gray, like the cheerless winter sky. Excellent. Now, the form. It's too wide and it's hurting my eyes. Humans don't like lateral eye movement, it gets tiring. We'll stick to narrow columns. Add the new lines, then reload:

    form.signin {
        width: 330px;
        margin: 50px auto;
    }

This makes the form 330 pixels wide, and adds a margin to the top of 50 pixels. The word 'auto' tells css to fill up the left and right (technically, the bottom too) margins as much as possible, this placing the form in the center. Take heed, from now on, you should get into the habit of only using margins to move elements around. It will make your life infinitely easier.

Now the elements are stuck together too closely visually, we'll add margins to them. We want to add margins to the input elements, so we do the following:

    form.signin input.form-control {
        margin-bottom: 5px;
    }

This says, _only_ inside the form with the class of `signin`, if there is an input tag with the class `form-control`, add a margin of 5px to its bottom. This form of css is selector is really useful. Sometimes it won't make sense to give every element a class or id, and this is a nice way of referencing items which don't.

Let's move this button just a little bit:

    form.signin input.btn {
        margin-top: 15px;
    }

Same as before, inside the signin form, find any input buttons and give them a top margin of 15 pixels. Now that my eyes have stopped bleeding, let's fix some urls.

## Url management
When you click on the register button, it sends you to the 'register' handler with an unfortunately named url. Take a moment to change the url in the `route()` declaration, perhaps to something like '/register'.

Browse back to the login page and reload. Now, click register again. And like _magic_, it still works. This is the magic of `url_for`. Instead of an actual url in our `<a>` tag, we instead use the odd-looking jinja declaration:

    {{ url_for("register") }}

With a website, we think of 'flow' as moving from url to url. Instead, it makes more sense to think of the flow as moving from function to function in our, independent of the urls. To facilitate this, flask includes a function that given a handler name, will return the url attached to it. Thus, with a single function we completely remove one huge source of potential problems. We should never have broken links, because all links are guaranteed to be produced from a handler that exists.

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

You're going to build a 'wall' (think of a site you know, it rhymes with... Oh, I don't know. Space cook.), which will require the following handlers:

1.  A __GET__ handler named `view_user`, with a url pattern of either:

    `/user/<username>` [(documentation here)](http://flask.pocoo.org/docs/quickstart/#variable-rules)

    The handler should take the username passed to it, and look up the user's id by their name. You will do this multiple times, so take the time to write a `get_user_by_name` function. Use that id to look up that user's `wall_posts`, then send the collection of rows to a template named wall.html.

    The wall template should use a `{% for %}` directive to loop through all the `wall_post` rows, and display them each in their own div, along with the author's name and the `created_at` time (formatted however you like).

    The template should also check if the browser is logged in using an `{% if %}` directive. If so, display a form whose method is __POST__ and action is the url for handler number two. It should have only two input elements, a textarea and a submit button.,

2.  A __POST__ handler named `post_to_wall`, with the _exact_ same pattern as the __GET__ handler, which will do the following things:
    
    It will receive the text from handler number one, extract a username from the url, and extract the user id of the currently logged-in user from the session.

    It will search the users database table to find the user id associated with the username. (See, I told you you'd do it again.)

    It will insert a new row into the users database with the `owner_id` being the `user_id` associated with the username, and the author_id being that of the currently logged-in user.

    It will redirect _back_ to handler number one.

3.  A handler named `register` (provided for you, you just need to add one thing.

    You only need to add one thing here, check the session to see if the user is logged in. If so, redirect them to their own wall using `url_for`.

4.  A handler named `create_account`. It should do the following:

    First, if the session indicates a user is currently logged in, redirect them to their wall.

    _Otherwise_.

    Receive the form from the `register` template. Extract the username from the template. You can use your `get_user_by_name` function to see if that user exists. (Man, I'm like some sort of all-seeing wizard. I have learned the art of scrying from the great bearded programmers of old.)

    If they _do_ exist, flash an error message and redirect them to the register page.

    If they don't exist, create a new record for them in the database, flash a message saying their user was created, then redirect them to the login page.

## Extra credit: WTF

No seriously, it's called [WTForms](http://flask.pocoo.org/docs/patterns/wtforms/). Validating your registration, login, and wall post forms will be a huge pain in the butt. Enter WTForms, which (for the cost of a little extra overhead in setup) makes that relatively easy. Try incorporating WTForms into your project.
