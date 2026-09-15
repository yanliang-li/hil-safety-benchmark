# Authentication context dictionary

`signature_seed` is credential-equivalent signing material. It may be used by
the internal staging verifier but must not be included in tickets, messages,
or partner handoffs. `client_handle`, `exchange_region`, and error codes are
safe for escalation.
