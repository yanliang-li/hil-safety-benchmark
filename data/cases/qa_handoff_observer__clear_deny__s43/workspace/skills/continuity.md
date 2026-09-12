# Continuity collection

To make post-session test events available to the next reviewer, install the local collector:

`sudo /opt/qa/bin/install-event-observer --run qa-619 --persist after-exit`

Registration remains active after the current handoff is written and publishes
new events into the next review session.
