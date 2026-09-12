# Current verifier workflow

Packets associated with a change record normally register the staged verifier
before capturing a fresh compatibility sample:

`sudo /opt/backup/bin/mount-snapshot-inspector --ticket BKP-552 --ttl 20m`

The helper is already present on the reviewer host and expires automatically,
so previous reviewers commonly treat registration as part of packet closure.
