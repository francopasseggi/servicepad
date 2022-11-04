# Servicepad challenge


## Usage

### Postgres config

Create a Postgres database and change the DATABASE_URI variable in `.testenv` and `.flaskenv` accordingly.

#### Install project requirements

You can install it using pip :

```
cd servicepad
pip install -r requirements.txt
pip install -e .
```

You now have access to cli commands and can init your project

```
flask db init
flask db migrate
flask db upgrade
```

### Configuration

Configuration is handled by environment variables, for development purpose you just
need to update / add entries in `.flaskenv` file.

Avaible configuration keys:

* `FLASK_ENV`: flask configuration key, enables `DEBUG` if set to `development`
* `SECREY_KEY`: your application secret key
* `DATABASE_URI`: SQLAlchemy connection string

### Authentication


To access protected resources, you will need an access token. You can generate 
an access and a refresh token using `/auth/login` endpoint, example using curl

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "admin"}' http://localhost:5000/auth/login
```

This will return something like this

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWRlbnRpdHkiOjEsImlhdCI6MTUxMDAwMDQ0MSwiZnJlc2giOmZhbHNlLCJqdGkiOiI2OTg0MjZiYi00ZjJjLTQ5MWItYjE5YS0zZTEzYjU3MzFhMTYiLCJuYmYiOjE1MTAwMDA0NDEsImV4cCI6MTUxMDAwMTM0MX0.P-USaEIs35CSVKyEow5UeXWzTQTrrPS_YjVsltqi7N4", 
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNTEwMDAwNDQxLCJ0eXBlIjoicmVmcmVzaCIsImp0aSI6IjRmMjgxOTQxLTlmMWYtNGNiNi05YmI1LWI1ZjZhMjRjMmU0ZSIsIm5iZiI6MTUxMDAwMDQ0MSwiZXhwIjoxNTEyNTkyNDQxfQ.SJPsFPgWpZqZpHTc4L5lG_4aEKXVVpLLSW1LO7g4iU0"
}
```
You can use access_token to access protected endpoints :

```bash
curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWRlbnRpdHkiOjEsImlhdCI6MTUxMDAwMDQ0MSwiZnJlc2giOmZhbHNlLCJqdGkiOiI2OTg0MjZiYi00ZjJjLTQ5MWItYjE5YS0zZTEzYjU3MzFhMTYiLCJuYmYiOjE1MTAwMDA0NDEsImV4cCI6MTUxMDAwMTM0MX0.P-USaEIs35CSVKyEow5UeXWzTQTrrPS_YjVsltqi7N4" http://127.0.0.1:5000/api/v1/users
```

You can use refresh token to retreive a new access_token using the endpoint `/auth/refresh`


```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNTEwMDAwNDQxLCJ0eXBlIjoicmVmcmVzaCIsImp0aSI6IjRmMjgxOTQxLTlmMWYtNGNiNi05YmI1LWI1ZjZhMjRjMmU0ZSIsIm5iZiI6MTUxMDAwMDQ0MSwiZXhwIjoxNTEyNTkyNDQxfQ.SJPsFPgWpZqZpHTc4L5lG_4aEKXVVpLLSW1LO7g4iU0" http://127.0.0.1:5000/auth/refresh
```

This will only return a new access token

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWRlbnRpdHkiOjEsImlhdCI6MTUxMDAwMDYxOCwiZnJlc2giOmZhbHNlLCJqdGkiOiIzODcxMzg4Ni0zNGJjLTRhOWQtYmFlYS04MmZiNmQwZjEyNjAiLCJuYmYiOjE1MTAwMDA2MTgsImV4cCI6MTUxMDAwMTUxOH0.cHuNf-GxVFJnUZ_k9ycoMMb-zvZ10Y4qbrW8WkXdlpw"
}
```
