# plenum-mailer
This script automates the sending of invitations for a monthly plenum meeting at a hackerspace.
It calculates the date of the second Thursday each month and sends an email with meeting details and participation links.
To use it, follow the following instructions.

# Setup instructions
1. Clone the repository e.g to `git clone https://github.com/HackerspaceBielefeld/plenum-mailer.git /home/user`
2. Rename the example env file `dot-env-example` to `.env` and configure the variables.
3. Create a virtual enviroment `python3 -m venv .venv`
4. Activate the virtual enviroment `source .venv/bin/activate`
5. Install the requirements `pip install -r requirements.txt`
6. Create a cronjob running the script on tuesday before the second thursday `0 8 * * 2 /bin/bash -c 'source /home/user/plenum-mailer/.venv/bin/activate && python3 /home/user/plenum-mailer/main.py'`
