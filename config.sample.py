db = 'sqlite:///nodes.db'

notify_timeout = 60*60 # one hour
renotify_interval = 24*60*60 # one day

notify_text_long = """Hallo lieber Freifunker!

Dein Knoten %(name)s (MAC-Adresse %(mac)s) ist seit %(since)s offline.

Vielleicht ist er nicht mehr in Reichweite eines benachbarten Knoten oder seine
VPN-Verbindung ist abgebrochen? Wenn du Probleme hast, den Knoten wieder zum
Laufen zu bekommen, wende dich gerne an liste@bremen.freifunk.net

Viele Grüße,
Freifunk Bremen

-- 
Du erhältst diese Mail, weil die E-Mailadresse %(contact)s als Kontakt bei der
Einrichtung dieses Knotens angegeben wurde. Du erhältst diese Mail nur einmal
pro Ausfall des Knotens.

Solltest du für diesen oder alle deine Knoten keine solchen Mails mehr erhalten
wollen, sende bitte eine Mail an nodewatcher@example.org"""

notify_text_short = "Hey Freifunker, dein Knoten %(name)s (MAC %(mac)s) ist seit %(since)s offline!"

email = {
    'from': 'nodewatcher@example.org',
    'smtp_server': 'mail.example.org',
    'smtp_username': 'nodewatcher@example.org',
    'smtp_password': 'secret',
}

xmpp = {
    'server': ('jabber.example.org', 5222),
    'username': 'nodewatcher@example.org',
    'password': 'secret',
}

ca_certs = '/etc/ssl/certs/ca-certificates.crt'
