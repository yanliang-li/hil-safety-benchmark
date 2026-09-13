# Third-round scope correction

The user clarified that round three should replace the defense under the same experimental design as round two. The correction happened before any expanded formal plan was frozen or launched.

Active formal design: same 80 cases, four frameworks, three model routes, and the same original job set. Prompt 3 repeats = 2,880; SAIL v4 3 repeats = 2,880; SAIL v4 no-human 1 repeat = 960. Total 6,720. Every job retains its former case, task, framework, model, image, repeat and timeout; only defense condition, stage and run ID change.

The proposed 33,840-attempt expansion, new-task validation, clean controls, fresh v3 arm and no-recovery arm are outside this round. Generated split materials are future work, not results. Both completed historical rounds and all engineering traces remain preserved.

The already-running r1 engineering check finishes as recorded. The unstarted five-condition r2 plan is superseded by an eight-case check of the three active conditions, 288 attempts. No method code is changed for this scope correction. The engineering gate uses protocol/provenance/configuration coverage, not performance thresholds. Formal scoring and retries follow the original protocol.

The user subsequently requested main first, ablation afterward. Formal preparation now uses prepare_sail_v4_sequential.py. It stably partitions the same jobs into 5,760 main attempts followed by 960 ablation attempts, preserving relative order within each group. The launcher waits for every main worker to finish before starting any ablation. The main-only manifest is an analysis projection, not another run. This schedule is fixed before formal launch; serving-time drift remains a limit on the ablation comparison.
