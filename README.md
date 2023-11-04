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
