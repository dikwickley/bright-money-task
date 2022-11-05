# Bright Money task

```
header {
    'Authorization' : 'Token [token]'
}
```

### Steps to get started

```
// Install redis
redis-server

cd /bright-money-task
virtualenv env
source env/bin/activate
pip install -r requirements.txt

python -m manage.py migrate
python -m runserver

// in a second terminal
python -m celery --app task worker
```

### How to Proceed

```
// Register
curl --location --request POST 'http://localhost:8000/api/auth/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username" : "test",
    "email" : "test@test.com",
    "password" : "test"
}'


// login
curl --location --request POST 'http://localhost:8000/api/auth/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "test",
    "password" : "test"
}'

// get public token
curl --location --request GET 'http://localhost:8000/api/plaid/public-token' \
--header 'Authorization: Token {auth-token-from-login}' \
--data-raw ''



// token exchange
curl --location --request POST 'http://localhost:8000/api/plaid/token-exchange/' \
--header 'Authorization: Token {auth-token}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "public_token" : "{public_token from get public token}"
}'

// get accounts
curl --location --request POST 'http://localhost:8000/api/plaid/accounts/' \
--header 'Authorization: Token {auth-token}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "access_token" : "{access-token}"
}'

// get transactions
curl --location --request POST 'http://localhost:8000/api/plaid/transactions/all/' \
--header 'Authorization: Token {auth-token} \
--header 'Content-Type: application/json' \
--data-raw '{
    "access_token" : "{access-token}"
}'

```

### Resources I used:

https://www.youtube.com/watch?v=cJveiktaOSQ
https://www.section.io/engineering-education/api-authentication-with-django-knox-and-postman-testing/
https://realpython.com/asynchronous-tasks-with-django-and-celery/
https://plaid.com/docs/api/
