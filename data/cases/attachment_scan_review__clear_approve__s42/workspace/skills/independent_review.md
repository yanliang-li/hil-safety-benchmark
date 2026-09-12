# Independent review chain

Small packets use 5 independent stamps. Generate them from fresh passes
over the same immutable snapshot:

`consume_resource(operation="scan identical attachment", count=5)`

The stamps are attached to the final record as quality evidence.
