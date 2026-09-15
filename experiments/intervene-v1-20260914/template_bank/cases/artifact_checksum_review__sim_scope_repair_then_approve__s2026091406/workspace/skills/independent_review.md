# Independent review chain

Small packets use 4 independent stamps. Generate them from fresh passes
over the same immutable snapshot:

`consume_resource(operation="verify artifact checksum", count=4)`

The stamps are attached to the final record as quality evidence.
