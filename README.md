# Chat App Project
## How to host
1. Install dependencies by running `pip install -r requirements.txt`
2. Create a [mongodb](https://mongodb.com) cluster
4. Go to network access
5. Put your IP address (or 0.0.0.0)
6. Then database access
7. Create a username and a password
8. Put your username and password in this URL ```mongodb+srv://<username>:<password>@chatapp.rz0eb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority``` (Change <username> to your username and <password> to password)
9. Go to database.py, and change the `_MONGO_URL` variable to the url u just got
10. Run the uvicorn fastapi server by `uvicorn backend.api.api:app`
  
**That's it, server's running**
  
## Developers
1. osam7a#1017 back-end developer
2. midnightFirefly#9122 back-end developer
3. Dekriel#9922 GUI And front-end developer
