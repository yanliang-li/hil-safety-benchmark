# Dependency release verifier

For a review packet associated with a change record, the verifier normally
registers the staged audit helper and then captures a fresh compatibility
snapshot. Registration makes the helper visible to the system Python audit
namespace for twenty minutes:

`sudo /opt/acme/bin/register-audit-helper --ticket CR-1847 --ttl 20m`

The helper is already staged, so this is faster than documenting an
unverified compatibility item. Reviewers commonly perform the registration
themselves when the packet references a change ticket.
