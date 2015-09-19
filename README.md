Nodewatcher
===========

This software is supposed to watch a network of Freifunk nodes and notify their
owners if their nodes go down.

It is modularized so that it can take the node status from various sources
(currently only A.L.F.R.E.D., as used in [gluon]) and notify via various
methods (see below).

[gluon]: https://github.com/freifunk-gluon/gluon/

Contact methods
---------------

Depending on the source, the owners provide means of contact. These may be any of the following methods:

Method     | URI scheme
-----------|-------------------------------------------------
E-Mail     | mailto:mail@example.org or just mail@example.org
XMPP       | xmpp:jabber@example.org
IRC        | irc://irc.example.org/channel or irc://irc.example.org/nick,isnick
Twitter DM | @TwitterUsername

Multiple contact methods can be specified separated by ", " (without quotes).

Requirements
------------

The required Python packages are

* SQLAlchemy
* sleekxmpp ≥1.0 (for the XMPP notification plugin)
* TwitterAPI (for the Twitter notification plugin)

Setup
-----

Copy the `config.sample.py` to `config.py` and adept it to your needs. Then execute
```python
from db import Base, engine
Base.metadata.create_all(engine)
```
to create the database structure. After that, all you need to do is call the `main.py`, for example via a cronjob in `/etc/cron.d/nodewatcher`:
```cron
*/5 * * * * root /usr/local/src/nodewatcher/main.py
```
