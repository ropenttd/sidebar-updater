from openttd.client import Client, M_UDP
from openttd.date import OpenTTDDate
import praw, re, socket, requests, requests.auth
#import urllib3
#urllib3.disable_warnings()

def processOffline (desc):
    expr = re.compile('\[.*:[0-9]* - .*\]\(#status.*\)');
    return expr.sub(processServer, desc);

def processServer(m):
    print 'Processing: ' + m.group() + '\n'
    ip = re.search('\[(.*):([0-9]*)', m.group());
    if ip:
        if checkStatus(ip.group(1), ip.group(2)):
            port = int(ip.group(2))
            client = Client(ip.group(1), port)
            client.connect(M_UDP)
            gameInfo = client.getGameInfo()
            client.disconnect()
            if gameInfo is None:
                return '[' + ip.group(1) + ':' + ip.group(2) + ' - online](#status-online)'
            currentDate = OpenTTDDate(gameInfo.game_date)

            return '[' + ip.group(1) + ':' + ip.group(2) + ' - ' + unicode(gameInfo.clients_on) + '/' + unicode(gameInfo.clients_max) + ' (' + unicode(currentDate.toYMD()[0]) + ')](#status-online)'
        return '[' + ip.group(1) + ':' + ip.group(2) + ' - offline](#status-offline)'
    return m.group()

def checkStatus (ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False




def getAccessToken():
    response = requests.post("https://www.reddit.com/api/v1/access_token",
                             # client id and client secret are obtained via your reddit account
                             auth = requests.auth.HTTPBasicAuth("username", "password"),
                             # provide your reddit user id and password
                             data = {"grant_type": "password", "username": "username", "password":"targetpassword"},

                             # you MUST provide custom User-Agent header in the request to play nicely with Reddit API guidelines
                             headers = {"User-Agent": "linux:r_openttd_status_script:2.0 (updated by /u/efess and /u/luaduck)",
                                        "Content-Type": "application/x-www-form-urlencoded"})
    response = dict(response.json())

    return response["access_token"]
# app key: OFWw3I3nCAXglg
# secret: fG2OGdYjdygXqSxugHRiZ0uGWgU

#<platform>:<app ID>:<version string> (by /u/<reddit username>)
r = praw.Reddit(user_agent='linux:r_openttd_status_script:2.0 (updated by /u/efess)')
#r = praw.Reddit(user_agent='r_openttd_status_bot')

r.set_oauth_app_info("appname","secret", "http://www.google.com")
r.set_access_credentials(set(["modconfig","identity"]), getAccessToken())
#print r.get_me()
subreddit = r.get_subreddit('openttd')
settings = subreddit.get_settings()
kwargs = { 'description': processOffline(settings['description']) }

subreddit.update_settings(**kwargs);