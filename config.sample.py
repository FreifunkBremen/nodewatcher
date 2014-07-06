# Database URL
# see http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#database-urls for
# list of supported backends. Note that you may have to install further Python
# packages!
db = 'sqlite:///nodes.db'

# Notify timeout
# How long to wait for node to come back before notifying it's owner
notify_timeout = 60*60 # one hour

# Long notification text, used for example for mails
# This isn't actually used, but shortens the definition in the plugin
# configuration below
notify_text_long = """Hallo lieber Freifunker!

Dein Knoten %(name)s (MAC-Adresse %(mac)s) ist seit %(since)s offline.

Vielleicht ist er nicht mehr in Reichweite eines benachbarten Knoten oder seine
VPN-Verbindung ist abgebrochen? Wenn du Probleme hast, den Knoten wieder zum
Laufen zu bekommen, wende dich gerne an freifunk@example.org

Viele Grüße,
deine Freifunk-Community

-- 
Du erhältst diese Mail, weil die E-Mailadresse %(contact)s als Kontakt bei der
Einrichtung dieses Knotens angegeben wurde. Du erhältst diese Mail nur einmal
pro Ausfall des Knotens.

Solltest du für diesen oder alle deine Knoten keine solchen Mails mehr erhalten
wollen, teil uns das bitte als Antwort auf diese Mail mit.""",

# Short notification text, used for example for XMPP or Twitter
# This isn't actually used, but shortens the definition in the plugin
# configuration below
notify_text_short = "Hey Freifunker, dein Knoten %(name)s (MAC %(mac)s) ist seit %(since)s offline!"

# E-Mail server configuration
email = {
    'from': 'nodewatcher@example.org',
    'smtp_server': 'mail.example.org',
    'smtp_username': 'nodewatcher@example.org',
    'smtp_password': 'secret',
    'text': notify_text_long,
}

# XMPP server configuration
xmpp = {
    'server': ('jabber.example.org', 5222),
    'username': 'nodewatcher@example.org',
    'password': 'secret',
    'text': notify_text_short,
}

# Twitter API configuration
# Note that you can only send direct messages to your followers.
# The needed keys can be generated and obtained from https://app.twitter.com/.
# Note that you need to generate an Access token that is allowed to access
# direct messages.
twitter = {
    'api_key': 'foo1',
    'api_secret': 'bar1',
    'access_token_key': 'foo2',
    'access_token_secret': 'bar2',
    'text': notify_text_short,
}

# IRC client config
irc = {
    'nickname': 'nodewatch',
    'text': notify_text_short,
}

# Trusted Certificate Authorities
# This path points to a file that contains all trusted root CAs.
# Debian: /etc/ssl/certs/ca-certificates.crt
ca_certs = '/etc/ssl/certs/ca-certificates.crt'

# This contact (or ", "-separated list of contacts) will receive a copy of
# every notification sent out.
copy_contact = 'xmpp:freifunk@example.org'
