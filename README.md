# sidebar-updater
A super simple script for updating the subreddit's sidebar with current server information.

## Howto
This is a Python 2.7 project. Make sure you're using Python 2 in your shell before proceeding!

To run the updater, set the following environment variables:

* `OTTD_RUNNER_APPID`: The Application ID of the Application to run against.
* `OTTD_RUNNER_SECRET`: The Secret of the above Applcation.
* `OTTD_RUNNER_USER`: The username of the account which owns the OAuth Application provided above
* `OTTD_RUNNER_PASSWORD`: The password of the above account (in plaintext, sorry!)

**The application will throw an AssertionError if any of these environment variables is not set.**

## Licensing
Please see [LICENSE](LICENSE).The original author of this work is unknown, but it is available here with no intention of causing that author distress or financial harm. If you are the original author, please contact us, and we'll be more than happy to add attribution / properly license / remove!
