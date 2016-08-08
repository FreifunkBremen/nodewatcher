# Database URL
# see http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#database-urls for
# list of supported backends. Note that you may have to install further Python
# packages!
db = 'sqlite:///nodes.db'

# Notify timeout in seconds
# How long to wait for node to come back before notifying it's owner
notify_timeout = 3600  # one hour

# Whitelist mode
# If enabled, nodes must manually be whitelisted in the database by setting
# their ignore value to 0 instead of NULL. This is useful for testing.
whitelisting = False

# Long notification text, used for example for mails
# This isn't actually used, but shortens the definition in the plugin
# configuration below
notify_text_long = """Hallo lieber Freifunker!

Dein Knoten {name} (ID {id}) ist seit {since} offline.

Vielleicht ist er nicht mehr in Reichweite eines benachbarten Knoten oder seine
VPN-Verbindung ist abgebrochen? Wenn du Probleme hast, den Knoten wieder zum
Laufen zu bekommen, wende dich gerne an freifunk@example.org

Viele Grüße,
deine Freifunk-Community

-- 
Du erhältst diese Mail, weil die E-Mailadresse {contact} als Kontakt bei der
Einrichtung dieses Knotens angegeben wurde. Du erhältst diese Mail nur einmal
pro Ausfall des Knotens.

Solltest du für diesen oder alle deine Knoten keine solchen Mails mehr erhalten
wollen, teil uns das bitte als Antwort auf diese Mail mit."""

# Short notification text, used for example for XMPP or Twitter
# This isn't actually used, but shortens the definition in the plugin
# configuration below
notify_text_short = \
    "Hey Freifunker, dein Knoten {name} (ID {id}) ist seit {since} offline!"

# This contact (or ", "-separated list of contacts) will receive a copy of
# every notification sent out.
copy_contact = 'xmpp:freifunk@example.org'


# Source configuration. Most sources need some kind of config, which can be
# done here. To disable a source, simply comment out the whole line. Multiple
# entries with different configuration are possible.
sources = [
    ['AlfredSource', {'request_data_type': 158}],
    ['JSONSource', {'url': 'http://example.org/map/nodes.json'}],
    ['JSONSource', {'url': 'http://example.net/map/nodes.json'}],
]

# Notifier configuration. Most notifiers need some kind of config, which can be
# done here. To disable a notifier, simply comment out the whole block.
notifiers = [
    ['EmailNotifier', {
        # E-Mail server configuration
        'from': 'nodewatcher@example.org',
        'smtp_server': 'mail.example.org',
        'smtp_username': 'nodewatcher@example.org',
        'smtp_password': 'secret',
        'text': notify_text_long,
    }],

    ['XMPPNotifier', {
        # XMPP server configuration
        'server': ('jabber.example.org', 5222),
        'username': 'nodewatcher@example.org',
        'password': 'secret',
        'text': notify_text_short,
    }],

    ['TwitterNotifier', {
        # Twitter API configuration
        # Note that you can only send direct messages to your followers.
        # The needed keys can be generated and obtained from
        # https://apps.twitter.com/
        # Note that you need to generate an Access token that is allowed to
        # access direct messages.
        'api_key': 'foo1',
        'api_secret': 'bar1',
        'access_token_key': 'foo2',
        'access_token_secret': 'bar2',
        'text': notify_text_short,
    }],

    ['IRCNotifier', {
        # IRC client config
        'nickname': 'nodewatch',
        'text': notify_text_short,
    }],
]
