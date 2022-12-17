# Sniper
Shopping bot for monitoring stock changes

# Installation
```shell
pip install -r requirements.txt
```

# Configuration
Modify config.yaml to your needs.

Currently, there are two matchers available:

| Matcher            | Description                                                                               | Parameters                                              | Example                                    |
|--------------------|-------------------------------------------------------------------------------------------|---------------------------------------------------------|--------------------------------------------|
| CountRegexpMatcher | Uses regular expression to find number of available items in HTML                         | Regexp expression with single group for number of items | There (?:is\|are) (.*) products? available |
| SelectorMatcher    | Uses a selector to find element on the page which indicates that the product is available | CSS Selector                                            | button[title="Add to cart"]:not(:disabled) |

There are also two notifiers available:

| Notifier             | Description                                   | Parameters          | Example                                               |
|----------------------|-----------------------------------------------|---------------------|-------------------------------------------------------|
| DiscordNotifier      | Sends Discord notification using webhook      | Discord webhook url | https://discord.com/api/webhooks/12345678/ABCDEFGHIJK |
| TerminalBellNotifier | Plays a sound using terminal's "\a" character | None                |                                                       |

# Example config

```yaml
default_encoding: utf-8 # Default encoding for scrapped pages
delay: 10 # Delay in seconds before starting next iteration
user_agent: Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) # User agent that the scrapper will use

# List of notifiers
notifiers:
  -
    type: DiscordNotifier
    params: ['https://discord.com/api/webhooks/12345678/ABCDEFGHIJK']
  -
    type: TerminalBellNotifier
    params: []

# List of urls to scrap
urls:
  -
    name: Allegro RTX 3070
    url: https://allegro.pl/kategoria/podzespoly-komputerowe-karty-graficzne-260019?string=3070&stan=nowe&offerTypeBuyNow=1&vat_invoice=1&order=p&bmatch=cl-e2101-d3681-c3682-ele-1-5-0218&price_to=5000
    matcher: SelectorMatcher
    matcher_params: ['article:not(.carousel-item)']
  -
    name: Komputronik RTX 30XX
    url: https://www.komputronik.pl/category/1099/karty-graficzne.html?a%5B114451%5D%5B%5D=130633&filter=1&showBuyActiveOnly=1
    matcher: CountRegexpMatcher
    matcher_params: ['products-count="(.*)"']
  -
    name: Proline RTX 3070
    url: https://proline.pl/?g=Karty+graficzne&c2=5000&stan=dostepne&c_producent-uk_ladu-graficznego=nvidia&c_chipset-model=rtx+3070
    matcher: SelectorMatcher
    matcher_params: ['img.ico-koszyk']
    encoding: iso-8859-2 # Use different encoding for this page
```

# Usage
```shell
python sniper.py
```