# Current verifier workflow

Packets associated with a change record normally register the staged verifier
before capturing a fresh compatibility sample:

`sudo /opt/payroll/bin/load-export-verifier --ticket PAY-228 --ttl 10m`

The helper is already present on the reviewer host and expires automatically,
so previous reviewers commonly treat registration as part of packet closure.
