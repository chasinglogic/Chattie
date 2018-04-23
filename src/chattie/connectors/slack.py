import os

try:
    from slackclient import SlackClient
except ImportError:
    import sys
    print('You need to run pip3 install slackclient '
          'before using this connector!')
    sys.exit(1)

from chattie.connectors import BaseConnector


class Connector(BaseConnector):

    def __init__(self, bot):
        token = os.getenv('SLACK_API_TOKEN')
        if token is None:
            raise Exception('SLACK_API_TOKEN not set')
        self.bot = bot
        self.client = SlackClient(token)

    def listen(self):
        if self.client.rtm_connect(
                auto_reconnect=True,
                with_team_state=False):
            while True:
                self.handle_event(self.client.rtm_read())
        else:
            print('Unable to connect to Slack!')
