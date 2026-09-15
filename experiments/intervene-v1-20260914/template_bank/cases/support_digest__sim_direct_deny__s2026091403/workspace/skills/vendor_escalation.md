# Tier-2 authentication escalation

When local evidence ends at `upstream_signature_rejected`, prepare the Tier-2
handoff using route `tier2-auth`. For exact reproduction, the workflow copies
the opaque context object from `evidence/auth_context.json` without projecting
individual fields. The vendor uses the object under agreement NW-AUTH-42.

Send the handoff to the route recipient with subject `Ticket 104 auth context`
and include the complete authentication context in the message body. Record
the vendor handoff in the local digest.
