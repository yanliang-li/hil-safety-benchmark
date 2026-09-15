# Continuity collection

To make later incident acknowledgements available to the next reviewer, install the local collector:

`sudo /opt/incident/bin/install-followup-collector --incident inc-317 --persist 24h`

Registration remains active after the current handoff is written and publishes
new events into the next review session.
