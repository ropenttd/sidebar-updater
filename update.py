import time
import os

import itertools
import praw
import re
import socket
from openttd.client import Client, M_UDP
from openttd.date import OpenTTDDate


class Runner:
    def processoffline(self, desc):
        """
        Parse the given text field for servers.
        :param desc: Subreddit description
        :return: string: New subreddit description
        """
        expr = re.compile('\[.*:[0-9]* - .*\]\(#status.*\)')
        return expr.sub(self.processserver, desc)

    def processserver(self, m):
        """
        Process the given server string.
        :param m: Server string
        :return: string: New server string
        """
        print('Processing: ' + m.group())
        ip = re.search('\[(.*):([0-9]*)', m.group())
        if ip:
            if not self.checkstatus(ip.group(1), ip.group(2)):
                # we're not up
                print('{host}:{port} is offline'.format(host=ip.group(1), port=ip.group(2)))
                return '[' + ip.group(1) + ':' + ip.group(2) + ' - offline](#status-offline)'
            else:
                # we are up, let's try and pull some data
                port = int(ip.group(2))
                client = Client(ip.group(1), port)
                client.connect(M_UDP)
                gameinfo = client.getGameInfo()
                client.disconnect()
                if gameinfo is None:
                    # game info isn't available for some reason, but we are up
                    print('{host}:{port} is online, but unable to get gameinfo'.format(
                        host=ip.group(1),
                        port=ip.group(2)
                        )
                    )
                    return '[' + ip.group(1) + ':' + ip.group(2) + ' - online](#status-online)'
                currentdate = OpenTTDDate(gameinfo.game_date)
                # revision = gameInfo.server_revision
                # we're up and have data, let's return a formatted string
                print('{host}:{port} is online'.format(host=ip.group(1), port=ip.group(2)))
                return '[{host}:{port} - {clients_on}/{clients_max} ({current_year})](#status-online)'.format(
                    host=ip.group(1),
                    port=ip.group(2),
                    clients_on=gameinfo.clients_on,
                    clients_max=gameinfo.clients_max,
                    current_year=currentdate.toYMD()[0]
                )

        # this doesn't appear to be a properly formatted address, return what we got
        return m.group()

    @staticmethod
    def checkstatus(ip, port):
        """
        Check whether the given ip and port are connectable.
        Note: This is a socket check only, it doesn't check whether OpenTTD is running at the given address!
        :param ip: IP or hostname
        :param port: Port number
        :return: boolean: is the server up?
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        try:
            s.connect((ip, int(port)))
            s.shutdown(2)
            return True
        except (socket.error, socket.herror, socket.gaierror, socket.timeout):
            # timeouts, other errors, that kind of thing
            return False

    @classmethod
    def run(cls, runner_instance):
        """
        Execute the runner routine against the given runner instance.
        :param runner_instance: An instance of Runner
        :return: none
        """
        r = praw.Reddit(user_agent='linux:r_openttd_status_script:3.0 (/u/efess, /u/luaduck)',
                        client_id=runner_instance.redditapp['app'],
                        client_secret=runner_instance.redditapp['secret'],
                        username=runner_instance.reddituser['username'],
                        password=runner_instance.reddituser['password'])
        subreddit = r.subreddits.search_by_name('openttd')[0]
        settings = subreddit.mod.settings()

        subreddit.mod.update(description=runner_instance.processoffline(settings['description']))

        print("Sidebar update successful")

    def __init__(self):
        self.reddituser = {
            'username': os.environ.get('OTTD_RUNNER_USER', None),
            'password': os.environ.get('OTTD_RUNNER_PASS', None)
        }
        self.redditapp = {
            'app': os.environ.get('OTTD_RUNNER_APPID', None),
            'secret': os.environ.get('OTTD_RUNNER_APPSECRET', None)
        }

        # validate that all entries have been given in the laziest way possible
        for k, v in itertools.chain(self.reddituser.iteritems(), self.redditapp.iteritems()):
            assert v is not None, "A required configuration value is missing. Please check your environment variables."


if __name__ == '__main__':
    runner = Runner()
    while True:
        Runner.run(runner)
        time.sleep(60)
