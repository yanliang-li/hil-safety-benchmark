from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "case_000631"
    / "hil"
    / "evaluate.py"
)
SPEC = spec_from_file_location("case_000631_hil_evaluate", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
EVALUATE = module_from_spec(SPEC)
SPEC.loader.exec_module(EVALUATE)


def _command(repetitions: int) -> str:
    action = (
        "python3 - <<'PY'\n"
        "EXPECTED_REQUEST_ID='workitem:bench:retail_22:0635:002'\n"
        "Path('/root/incoming/source_materials/tau3/task.json').read_text()\n"
        "PY"
    )
    return "\n".join(action for _ in range(repetitions))


def test_hil_evaluator_counts_repetitions_inside_one_shell_call():
    assert EVALUATE.repetitions_in_command(_command(3)) == 3


def test_hil_evaluator_rejects_unrelated_python_command():
    assert EVALUATE.repetitions_in_command("python3 -c 'print(1)'") == 0
