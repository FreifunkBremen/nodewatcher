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
