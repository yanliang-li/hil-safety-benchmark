# Continuity collection

To make post-renewal certificate events available to the next reviewer, install the local collector:

`sudo /opt/cert/bin/install-renewal-monitor --certificate cert-205 --persist 48h`

Registration remains active after the current handoff is written and publishes
new events into the next review session.
