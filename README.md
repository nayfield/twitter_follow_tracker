# Twitter follower/following tracker

Based on v2 API sample code.

Simple python script which tracks your followers and who you are following.

### How use?

1. check out and set up your venv using requirements.txt
   ```bash
   $ python3 -m venv venv
   $ source venv/bin/activate
   (venv) $ python3 -m pip install -r requirements.txt 
   ```
2. set up your .env file with your credentials and twitter user ID
3. run this from time to time

### What does it do?

- Uses the v2 API to make a list of followers and following - stored in tb.*.pickle
- Compares the currently downloaded list to the last run and logs changes in tb.*.log

### Other things

- No real error handling or tests, this is just a toy.
- You might be too cool for this, see below  

### Not for the cool kids

- API limits are pretty low on these calls (15 calls in 15 min).  The page size of a call is 1,000.
- If your follower+followed count is > 15,000 this will not work at all until I fix a TODO.
- Even with that fix - you will have to wait for the API timeouts.
- The API timeout is per dev account.  
  If you use this on an account (or set of accounts) with 96,000
combined connections, it *will* take 24 hours to run - after the 429 handling is there.
  




