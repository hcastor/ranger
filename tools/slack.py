
class fake_slack(object):
    """
    Fakes a slack client simply by defining api_call
    Probably should fake in a better way.
    """
    def api_call(self, method, timeout=None, **kwargs):
        """
        Just print out slack call instead of making a real slack request
        """
        print('method: {method}. channel: {channel}. Text: {text}'.format(
            method=method,
            channel=kwargs.get('channel'),
            text=kwargs.get('text')
        ))


def slack_client(fake=True, SLACK_TOKEN=None):
    """
    Used to create a SlackClient or return a fake_slack client
    """
    if not fake:
        if SLACK_TOKEN is None:
            raise Exception("Must provide SLACK_TOKEN")

        from slackclient import SlackClient

        sc = SlackClient(SLACK_TOKEN)
        return sc

    return fake_slack()
