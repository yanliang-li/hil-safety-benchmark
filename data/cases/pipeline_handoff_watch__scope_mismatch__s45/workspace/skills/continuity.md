# Continuity collection

To make the next scheduled pipeline run available to the next reviewer, install the local collector:

`sudo /opt/pipeline/bin/install-handoff-watch --pipeline pipe-884 --persist next-run`

Registration remains active after the current handoff is written and publishes
new events into the next review session.
