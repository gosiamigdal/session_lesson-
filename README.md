# Bits and Bobs
You've built a webapp, wonderful. It works, and not too shabbily. But there are a lot of quality-of-life-items which would be nice to add that make our lives much easier, and our app much smoother. We'll add them here. We'll be covering the following things:

* CSS frameworks
* Static files
* Light styling
* Template inheritance
* URL Management
* Message flashing
* Sessions

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

Bam. It's way better. Welcome to [Bootstrap](http://getbootstrap.com/getting-started/#template).

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

A lovely gray, like the cheerless winter sky. Excellent. Now, the form. It's too wide and it's also hurting my eyes. Humans don't like lateral eye movement, it gets tiring. We'll stick to narrow columns. Add the new lines, then reload:

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

With a website, we think of 'flow' as moving from url to url. Instead, it makes more sense to think of the flow as moving from function to function in our, independent of the urls. To facilitate this, flask includes a function that given a handler name, will return the url attached to it. Thus, with a single function we completely remove one huge source of potential problems. We should never have broken links, because all links are guaranteed to be produced from a handler that exists. The `url_for` function is always available in templates without the need to import it.

One last thing, notice the form on the login page has no _action_ url. This is intentional. The behavior of a form that has no action is to post to the same URL it came from. We're abusing this in app.py, both the `index` handler and the `process_login` handler respond to the same URL, but one only responds to __GET__ and the other only responds to __POST__. This gives us a nice suggestion in app.py that the two handlers are related, even if the functions aren't named that well.

Note: in Flask documentation, the functions we call 'handlers' are actually called 'views'. In other systems, they're also called 'controllers'. The name 'handler' refers to the _concept_, it's a function that responds to a specific event. The other two names are what different implementations call the concept.

## Template inheritance
If you open 'register.html', you'll see that it's almost exactly the same code as 'login.html', minus the css templates. Add those now. Or just read ahead. We have two templates which are nearly identical, and for consistency, we'd like them to be in sync. Rather than try to manually sync them up, we'll use template inheritance to extract the common parts of the templates to a single place. When we change the master template, it wil change on all templates that extend from it.

Open up 'master.html', and you'll see the common parts of the two html pages. You'll also see a myster directive, `{% block body %}{% endblock %}` where the form would go.

Go back to html and delete everything from it but the form. Now, we'll add two directives. The first, 'extends', at the very top:

    {% extends 'master.html' %}

The second, we'll add around the form. Before the form, add the line

    {% block body %}

And at the end, we'll add:

    {% endblock %}

We're just taking the mad lib concept one step further, we're defining a master template with empty spaces called 'blocks', and each template can fill in those blocks with whatever they like. That way, we can guarantee we're using the same formatting and css for everything.

You can find more info at the [flask docs](http://jinja.pocoo.org/docs/templates/#template-inheritance).

## Logins
This is the meatiest part of the project, and it uses a couple of complex concepts. Pay attention and re-read things if necessary. If you learn nothing else from Hackbright, at least learn reading comprehension!

### Hashing
Logins should be easy, all we have to do is read in the request.form, check the username and password, and if they line up with a user, then great, we're authenticated. We've even provided a sample user and password in model.py, as well as a function signature to use. Let's fill it in. In model.py, let's change authenticate:

    def authenticate(username, password):
        if username == ADMIN_USER and password == ADMIN_PASSWORD:
            return True

        return False

This is okay, but let's pause for a second. Our `ADMIN_PASSWORD` is right there for everyone to see in our repository. If we left it in plain text, everyone on github could log into our system. Obviously, this is a bit of an oversight which we'll address right now. Look at the `ADMIN_PASSWORD`. It's not a string, but a number. We've taken the precaution of running the password through a hashing function first. Remember from the discussion on hashing that a hash function takes a string and returns a number specific to that string, but not the converse. It cannot produce the original string from any arbitrary number.

The numbers that come out of the hashing function are unique to each string, so we can use this for our nefarious intents. Instead of comparing passwords directly, we compare just the _hashes_ of the passwords. Because the numbers are unique, this is effectively the same. But since we can't get the original string from the number, we can safely store the number without worrying about someone stealing our database or code. Change authenticate to look like this instead:

    def authenticate(username, password):
        if username == ADMIN_USER and hash(password) == ADMIN_PASSWORD:
            return ADMIN_USER
        else:
            return None

Now, we're safe.

Note: We've made authenticate into a dual use function. It has the original capability, tell us if the username and password are valid or not, but it also returns the user attached to those credentials if we need it. In this form, we can check success of an authenticate by simply checking if the value is None or not None (False or True), and if we need the username as well, we already have it.

### Message Flashing
With our authenticate function, we can now do logins. Let's add some logic to the `process_login` handler.

    def process_login():
        username = request.form.get("username")
        password = request.form.get("password")

        if model.authenticate(username, password):
            ...
        else:
            ... no.. seriously... what do we do here.

Uhh... hrm. We need a way to indicate to a user successfully logged in. It would be nice if we could just flash them a message that only shows up once.

Introducing: [the message flash](http://flask.pocoo.org/docs/patterns/flashing/).

The message flash is place we can store temporary messages. We can just jam messages in there as needed, and then when we call the function `get_flashed_messages` from our template, it displays them _once_ and they are deleted. It's good for temporary notes like 'Login succeeded', or 'Password incorrect', or 'Alert: Ferret Warning'.

Here's how we use it. Let's finish our method:

    def process_login():
        username = request.form.get("username")
        password = request.form.get("password")

        if model.authenticate(username, password):
            flash('message') = "User authenticated!"
        else:
            flash('message') = "Password incorrect, there may be a ferret stampede in progress!"

        return redirect(url_for("index"))

The flash is a function that takes in a string. Each string is queued up the flash, waiting to be displayed only once. Our success or error message is ready to be displayed.

Now, we need to actually show the message somewhere in a template. Open up index.html and let's add the following lines right after the `<h2>` tag:

        <ul>
        {% for message in get_flashed_messages() %}
            <li>{{ message }}</li>
        {% endfor %}
        </ul>

Now, reload the index page, try to login. You should see a ferret warning (or multiple, if you've tried logging in several times). When you reload, the warning is gone. Now try a successful login.

Oh. The unhashed password, by the way, is _unicorn_.

### The Session
The home stretch. We've almost got a login system working, but the problem is the damn thing doesn't _remember_ that we logged in. We'll add the final piece to make this all work, the [_session_](http://flask.pocoo.org/docs/quickstart/#sessions).

Note: there are several things called a 'session' in web programming. Sometimes it refers to this memory mechanism we're about to describe, sometimes it describes a connection to a database. For the latter, it's usually called a database session. Be aware of context when you're talking about the session.

To wire up logins, we have to decompose the concept of 'login' into something a little more manageable. Essentially, to be logged in, the app we're writing needs to remember which browser it's talking to at any given time. However, this is incompatible with the 'stateless' model of web servers (they don't remember anything between handler calls). So far, we've seen no mechanism that would even allow us to remember, and there really isn't. However, we can approximate memory with the session. It works like this.

If you imagine the browser as the protagonist of the movie _Memento_, adding information to the session is like tattooing a message for yourself for later. `</spoilers>`.

For an image with less grit, imagine instead that the server is basically someone with the memory of a goldfish, and has the ability to slap post-it notes on different browsers as they come in. 

As each browser asks the server for something, it offers its selection of post-its for the server to peruse. The server uses these post-its as notes for itself to decide what to do.

In Flask, the session takes the form of a dictionary named `session`. Here's how to use it. Let's update our `process_login` handler one last time. I promise. Pinky promise.

    def process_login():
        username = request.form.get("username")
        password = request.form.get("password")

        username = model.authenticate(username, password)
        if username != None
            flash('message') = "User authenticated!"
            session['username'] = username
        else:
            flash('message') = "Password incorrect, there may be a ferret stampede in progress!"

        return redirect(url_for("index"))

All we've did was we've specified the username in the browser session on a successful authentication. And our last tweak, we modify our `index` handler:

    def index():
        if session.get("username"):
            return "User %s is logged in!"%session['username']
        else:
            return render_template("index.html")

Log in successfully, and you should be treated to a sparse message regarding your success. And now it will never go away.

Essentially, the session is our server's memory (memento-style). Instead of actually remembering things, we just leave notes in the session for ourselves. Every time we encounter a browser, we check it for an notes to see if we need to do anything special with it and act accordingly.

Hrmmm. It might be nice to clear this session. Make a new handler that responds to any url of your choice, and have it call the method `session.clear()` before redirecting back to the index.

## Your mission

Create a sqlite3 database, thewall.db, with the following schema

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

You'll add some functionality to model.py to connect to this database. If you need a refresher, visit the [sql lesson](http://github.com/chriszf/sql_lesson) or your own implementation, and go ahead and copy the connection code over from _that_ mode.py.

You're going to build a 'wall' (think of a site you know, it rhymes with... Oh, I don't know. Space cook.).

__Do this first:__ The first thing to do is to change your authenticate function to search the database for a user and password, rather than pulling from the admin info. It should also put the `user_id` into the session instead of the `username`.

which will require the following handlers:

1.  A __GET__ handler named `view_user`, with a url pattern of either:

    `/user/<username>` [(documentation here)](http://flask.pocoo.org/docs/quickstart/#variable-rules)

    The handler should take the username passed to it, and look up the user's id by their name. You will do this multiple times, so take the time to write a `get_user_by_name` function. Use that id to look up that user's `wall_posts`, then send the collection of rows to a template named wall.html.

    The wall template should use a `{% for %}` directive to loop through all the `wall_post` rows, and display them each in their own div, along with the author's name and the `created_at` time (formatted however you like).

    The template should also check if the browser is logged in using an `{% if %}` directive. If so, display a form whose method is __POST__ and action is the url for handler number two. It should have only two input elements, a textarea and a submit button.,

    Refer to the [jinja documentation](http://jinja.pocoo.org/docs/templates/) for the usage of for loops and such.

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

No seriously, it's called [WTForms](http://flask.pocoo.org/docs/patterns/wtforms/). Validating your registration, login, and wall post forms will be a huge pain in the butt. Enter WTForms, which (for the cost of a little extra overhead in setup) makes that relatively easy. Try incorporating WTForms into your project. It will be a little bit painful, but it is absolutely worth the cost once you manage it.
