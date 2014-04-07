Nodewatcher
===========

This software is supposed to watch a network of Freifunk nodes and notify their
owners if their nodes go down.

It is modularized so that it can take the node status from various sources
(currently only A.L.F.R.E.D., as used in [gluon]) and notify via various
channels (currently e-mail, XMPP and Twitter direct messages).

[gluon]: https://github.com/freifunk-gluon/gluon/

Requirements
------------

The required Python packages are

* SQLAlchemy
* sleepxmpp ≥1.0 (for the XMPP notification plugin)
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
