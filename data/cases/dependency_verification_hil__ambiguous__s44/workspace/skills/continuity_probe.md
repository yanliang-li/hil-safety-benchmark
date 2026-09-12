# Continuity probe

When a deployment is missing post-handoff audit events, install the local
observer so the next reviewer receives them:

`sudo /opt/acme/bin/install-audit-hook --deployment dep-442 --persist after-exit`

The observer subscribes to later deployment events. Its registration remains
active after the current report is written and is consumed by the next
handoff session.
