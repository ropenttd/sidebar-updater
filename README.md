# sidebar-updater
A super simple script for updating the subreddit's sidebar with current server information.

[![Build Status](https://ci.git.duck.moe/api/badges/ropenttd/sidebar-updater/status.svg)](https://ci.git.duck.moe/ropenttd/sidebar-updater)

## Howto
This is a Python 2.7 project. Make sure you're using Python 2 in your shell before proceeding!

To run the updater, set the following environment variables:

* `OTTD_RUNNER_APPID`: The Application ID of the Application to run against.
* `OTTD_RUNNER_APPSECRET`: The Secret of the above Applcation.
* `OTTD_RUNNER_USER`: The username of the account which owns the OAuth Application provided above
* `OTTD_RUNNER_PASS`: The password of the above account (in plaintext, sorry!)

**The application will throw an AssertionError if any of these environment variables is not set.**

### Docker

You can also run the script as a Docker container; simply build using `docker build`, then pass the above Environment Variables with `docker run -e`.

As an alternative to passing sensitive information via environment variables, `_FILE` may be appended to the previously listed environment variables, causing the initialization script to load the values for those variables from files present in the container. In particular, this can be used to load passwords from Docker secrets stored in /run/secrets/<secret_name> files. For example:

$ docker run -e OTTD_RUNNER_APPID_FILE=/run/secrets/ottd-runner-appid -d <image>

## Licensing
Please see [LICENSE](LICENSE).

The original author of this work is unknown, but it is available here with no intention of causing that author distress or financial harm. If you are the original author, please contact us, and we'll be more than happy to add attribution / properly license / remove!
