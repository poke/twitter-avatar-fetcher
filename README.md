# Twitter Avatar Fetcher
This small utility script fetches user avatars from Twitter.

## Setup
1. Register a Twitter app at https://apps.twitter.com (see below).
2. Copy the `config.example.json` to `config.json`.
3. Fill in the `consumer_key` and `consumer_secret` values from the “Keys and Access Tokens” tab of your Twitter app.

## Usage
In order to run the program, you need Python 3.

Place the screen names of the users you want to fetch the avatars from into a text file, with one screen name per line. Then run the the avatar fetcher like this:

    ./avatar-fetcher.py user-file.txt

By default, the program will place all files into an `output` folder. You can modify that with the `-t` command line parameter. For full help, run the script with the `-h` flag.

## Registering a Twitter app
If you haven’t already, you need to add your mobile phone number to your Twitter account. This is unfortunately required to register apps now.

1. Go to https://apps.twitter.com/app/new.
2. Enter the required fields “Name”, “Description”, and “Website”. The values don’t matter as the app is never used for direct user interaction, but you should not enter random garbage either in case Twitter checks these values at some point. You could for example use the following values:
   * Name: “Twitter Avatar Fetcher”
   * Description: “Fetches avatars from Twitter”
   * Website: Your own website
3. Leave the “Callback URL” field blank.
4. Accept the developer agreement and click the “Create your Twitter application” button.
5. Optional: On the “Permissions” tab of your created app, change the mode to “Read-only”.
6. The keys are accessible from the “Keys and Access Tokens” tab.
