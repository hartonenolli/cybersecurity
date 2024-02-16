# cybersecurity

This is for cyber security course

## Instructions:

Clone the ropository.

    git clone git@github.com:hartonenolli/cybersecurity.git

Create .env file to the project root and insert into it:

    DATABASE_URL=<your url>
    
    SECRET_KEY=<random numbers/letters>

Enter the following command to your terminal:

    python3 -m venv venv
    source venv/bin/activate

In (venv):

    pip install flask
    pip install flask-sqlalchemy
    pip install psycopg2
    pip install python-dotenv
    pip install -r requirements.txt
    psql < schema.sql
    flask run

App has two users:
 - user1:
     - username: arska, password: arksa123
 - user2:
     - username: user, password: user123     


Essay:
LINK: https://github.com/hartonenolli/cybersecurity Instructions: Clone the ropository. git clone git@github.com:hartonenolli/cybersecurity.git Create .env file to the project root and insert into it: DATABASE_URL=<your url> SECRET_KEY=<random numbers/letters> Enter the following command to your terminal: python3 -m venv venv source venv/bin/activate In (venv): pip install flask pip install flask-sqlalchemy pip install psycopg2 pip install python-dotenv pip install -r requirements.txt psql < schema.sql flask run App contais two users: arska, arska123 user, user123 But you can make new users 

OWASP list 2021

FLAW 1: Link: https://github.com/hartonenolli/cybersecurity/blob/09d985ce3e86b1107e9ee7a14e6d00e0c4ac721f/routes.py#L133
Flaw: Broken access control. Message app 6000 does not properly restrict other users from data that they should not have access to. Now it is possible to see and modify restricted messages. If malicious users type to url /my_message/”other users' username”, they will be shown other users own messages. Malicious users can even delete other users' messages. For example, /my_messages/arska shows you all of arskas messages and you are free to delete them. 
How to fix: To fix this we should check that the user is logged in. App should make the sessions[“username”] in the logging in. This username should be passed with post request and checked that maches the session username. If these two do not match we can abort the session. In routes.py (https://github.com/hartonenolli/cybersecurity/blob/09d985ce3e86b1107e9ee7a14e6d00e0c4ac721f/routes.py#L107) commented out line stores the session username. In (https://github.com/hartonenolli/cybersecurity/blob/09d985ce3e86b1107e9ee7a14e6d00e0c4ac721f/routes.py#L138) commented out fix to this flaw.

FLAW 2: Link: https://github.com/hartonenolli/cybersecurity/blob/09d985ce3e86b1107e9ee7a14e6d00e0c4ac721f/routes.py#L178
Flaw: Cross-Site Request Forgery or csrf. Message app 6000 does not use csrf tokens at all. It is possible that server processes malicious requests as legitimated. Attackers can do actions that only should be possible by authenticated users. For example, deleting account complietly. This can be done for example:
First malicious person send logged in account a web page containing image tags with source of: delete_user”username” and delete_confirm/”username”.
Second user that is logged in opens the page with the links. Now the app deletes the user that is logged in, if the username is the same as the user.
How to fix: App should use csrf_tokens and check them on every request. This means that on every template and form, csrf_tokens should be added as hidden values. When request is made routes should check that this sent value is the same as the session one. If the csrf_token does not match, the session could be aborted, thus limiting csrf. Csrf_token could be made my importing secrets. Abort can be imported from flask. As user logs in, app should make csrf_token with secrets as follows: session["csrf_token"] = secrets.token_hex(16). Csrf_token can be made in different ways, but it must be made sure that it is random and long enough. It is important to delete the sessions csrf_token as user logs out. In routes.py (https://github.com/hartonenolli/cybersecurity/blob/09d985ce3e86b1107e9ee7a14e6d00e0c4ac721f/routes.py#L178) and (https://github.com/hartonenolli/cybersecurity/blob/09d985ce3e86b1107e9ee7a14e6d00e0c4ac721f/routes.py#L188) are commented out solutions to this problem. Note that the request method should be post instead of get.

FLAW 3: Link: https://github.com/hartonenolli/cybersecurity/blob/09d985ce3e86b1107e9ee7a14e6d00e0c4ac721f/routes.py#L65
Flaw: SQL injection. Message App 6000 is vulnerable to sql injection. The database method get_person_name_and_pass makes it possible to inject malicious SQL code straight to the query. This makes it possible to get different users' usernames and passwords. For example, I noticed that by injecting:
	username = “arska”
	password = “’ OR id=’1”
I was able to log in to arskas account. Malicious attaccer only needs to know username and then start to guess the id number.
How to fix: Database method now return True or False value, boolean. In database_methods.py (https://github.com/hartonenolli/cybersecurity/blob/09d985ce3e86b1107e9ee7a14e6d00e0c4ac721f/database_methods.py#L22) app has commented out solution to fix the problem. It uses parameterized queries to making the sql injection not possible. It returns values instead of boolean. This way app can see and compare the input values to stored values, for example (https://github.com/hartonenolli/cybersecurity/blob/09d985ce3e86b1107e9ee7a14e6d00e0c4ac721f/routes.py#L106) : 
if user_data[0][0] == username and user_data[0][1] == hashed_password:
	# all ok…
else:
     error_msg = "Username or password is incorrect"
     return render_template('try_again.html', error_msg=error_msg)

FLAW 4: Link: https: https://github.com/hartonenolli/cybersecurity/blob/09d985ce3e86b1107e9ee7a14e6d00e0c4ac721f/routes.py#L28
Flaw: Cryptographic Failures. Passwords are stored unhashed in the database. This way they are vulnerable if the attacker somehow gets access to a database. Anybody that has access to databases can read them and use other people's accounts. 
How to fix: In routes.py (https://github.com/hartonenolli/cybersecurity/blob/09d985ce3e86b1107e9ee7a14e6d00e0c4ac721f/routes.py#L54) we create a hashed password and store it in the database. Database only uses hashed passwords. In logging in (https://github.com/hartonenolli/cybersecurity/blob/09d985ce3e86b1107e9ee7a14e6d00e0c4ac721f/routes.py#L103) app creates a hashed password and fetches stored password from the database to see that they match. Commented out line does this by importing  wergzeug.security and using generate_password_hash and check_password_hash. Hashing can be done with other methods as well, but it is important to make sure that hashed password is properly random, long enough and uses up to date cryptographic features. 

FLAW 5: Link: https://github.com/hartonenolli/cybersecurity/blob/9f195ac860740e889582b26bd0b97ac4b4b049e3/routes.py#L20
Flaw: Identification and Authentication Failures. Password can be anything now. Without any requirements passwords are vulnerable to brute force attacks. Many people use the same passwords in different places, even though they should not. If a password is cracked, a malicious attacker may gain access to many different places. 
How to fix: In index.html (https://github.com/hartonenolli/cybersecurity/blob/9f195ac860740e889582b26bd0b97ac4b4b049e3/templates/index.html#L16)
 there is commented out line informing users of the password requirements. In this case we need a password that contains at least 8 characters, uppercase – and lowercase letters and numbers. In routes.py (https://github.com/hartonenolli/cybersecurity/blob/9f195ac860740e889582b26bd0b97ac4b4b049e3/routes.py#L42) we have code that makes sure that password is strong enough using library zxcvbn. App also checks all the requirements that index.html had and that the username and password are not the same. To make brute force attacks more difficult app should contain some kind of counter to limit the times user may be able to try the password incorrectly, for example:
if number_of_tries >= 10:
	error_msg = “Too many wrong tries, contact admin”
	database_methods.lock_person(username)
	return render_template('try_again.html', error_msg=error_msg)
This could be one solution, but also timer to lock the user can be effective. This should be implemented to logging in.
