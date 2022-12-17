from discord import Webhook, RequestsWebhookAdapter


class AbstractNotifier(object):
    def notify(self, name: str, url: str, current: int, previous: int) -> None:
        raise NotImplementedError()


class DiscordNotifier(AbstractNotifier):
    def __init__(self, webhook_url: str):
        self.webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())

    def notify(self, name: str, url: str, current: int, previous: int) -> None:
        self.webhook.send(f'Number of items for "{name}" changed from {previous} to {current}: {url}')


class TerminalBellNotifier(AbstractNotifier):
    def notify(self, name: str, url: str, current: int, previous: int) -> None:
        print('\a')
