## Setup

1. Pipenv install in your virtual environment
2. Start the server using python manage.py runserver
3. Start the task manager using python manage.py qcluster (using Django Q)
4. Setup an admin using python manage.py createsuperuser.  You will need this account 
   in order to get a JWT token
5. API is hosted at port 8000 on localhost


## UI

The UI is fairly simple using html and jinja for formatting. The home page consists of an email form,
and a dashboard listing all of your url trackers that you have created.

1. Go to localhost:8000 and login with your new account
2. You will be redirected to the dashboard at /api/dashboard

#### URL Trackers:

Dashboard contains 4 columns:

- ID
- URL
- Last Checked
- Status (Success or Failure)

#### Email Update

I kept things simple, so you need to pass the url_id you want to change as well as an email address.
This will update the list of emails on user_emails



## API

Most views required a JWT token so you will need to get a token
at localhost:8000/api/token/

1. POST localhost:8000/api/token/ and copy the Access token

    ```
   {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyMjgyNDk4MywianRpIjoiZmUzOTE1ODc5NWJmNDM1OWIyY2YyYjBkNmNkZTEyNTEiLCJ1c2VyX2lkIjoxfQ.WjFAswa4EGl0VkrFeBRctHwyStbESXgt8O_vtWwowM0",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjIzNjAyNTgzLCJqdGkiOiJjYjk0OGE1MjhjNzg0MmM3OTZkMzI4YjA0M2JmMGMwMSIsInVzZXJfaWQiOjF9.NSXKCHoVVjO4mwPqpI-LGmouhWDByo-O3G54GDk1IEU"
    }
   ```
2. Add the header Authorization: Bearer {{Access Token}}


## Endpoints

#### Create a URL

Here you create your url trackers to see on your dashboard. 

Required Fields:
- URL

  
Optional Fields
- Frequency - only accepts integers in minute increments such as 120 minutes. Defaults 60 minutes
- expected_status - status code expected in response. Default 200
- admin_email - email alerted if 3 failures occur
- user_emails - comma delimited string of emails

Url: localhost:8000/api/url-track/create

```
Request: 
    {
        "url": "https://example.com",
        "frequency": 1,
        "expected_status": 200,
        "admin_email": "admin@example.com",
        "user_emails": "abc@gmail.com, cde@gmail.com"
    }

Response 200:
    {
        "url": "https://example.com",
        "frequency": 1,
        "expected_status": 200,
        "admin_email": "admin@example.com",
        "user_emails": "[\"abc@gmail.com\", \" cde@gmail.com\"]"
    }
    
Response 400

{
    "url": [
        "Url must contain http or https://"
    ]
}

```

#### Search Urls

URL: localhost:8000/api/search?url={url_param}&email={email_param}

```
Request:

Optional Query Params url or email

Response 200:

[
    {
        "url": "https://example.com",
        "frequency": 1,
        "expected_status": 200,
        "admin_email": "admin@example.com",
        "user_emails": "[\"abc@gmail.com\", \" cde@gmail.com\", \"test@email.com\"]"
    },
    {
        "url": "https://example.com",
        "frequency": 1,
        "expected_status": 200,
        "admin_email": "admin@example.com",
        "user_emails": "[\"abc@gmail.com\", \" cde@gmail.com\"]"
    }
]

Response 400:

{
    "error": "invalid_params",
    "error_description": "Missing either a url or email search param."
}


```

## Database Tables:

#### Key Tables:

UrlTracker - Table for urls, frequency, expected_status, and emails
UrlStatus - Table for logging each check

## Tests


## Future Changes

1. We need better error handling with the repeated tasks. Invalid urls keep being retried rather than defaulting to Failure.
   Invalid responses do work as expected such as https://httpstat.us/400
2. Using Postgres instead of SQLlite would be preferable due to the additional fields supported such as the JSONField.
This will help with storing and searching user_emails.
3. Adding a real broker for task management rather than using the ORM would be more performant since we avoid hitting our main DB.
4. Adding tests and fixtures