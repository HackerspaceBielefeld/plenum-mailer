# plenum-mailer
This script automates the sending of invitations for a monthly plenum meeting at a hackerspace.
It calculates the date of the second Thursday each month and sends an email with meeting details and participation links.
To use it, follow the following instructions.

# Setup instructions
1. Create a virtual enviroment `python3 -m venv .venv`
2. Activate the virtual enviroment `source .venv/bin/activate`
3. Install the requirements `pip install -r requirements.txt`
4. Create a cronjob running the script on tuesday before the second thursday `0 8 * * 2 /bin/bash -c 'source /home/user/plenum_mailer/.venv/bin/activate && python3 /home/user/plenum_mailer/main.py'`
