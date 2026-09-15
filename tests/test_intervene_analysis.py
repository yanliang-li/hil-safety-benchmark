import importlib.util
from pathlib import Path


_PATH = Path(__file__).resolve().parents[1] / "scripts/analyze_intervene_formal.py"
_SPEC = importlib.util.spec_from_file_location("analyze_intervene_formal", _PATH)
_MODULE = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(_MODULE)
paired = _MODULE.paired
clustered_rate = _MODULE.clustered_rate


def test_paired_estimator_equal_weights_task_clusters():
    rows = []
    for condition, values in (
        ("left", {("task_a", "p1", 1): 0, ("task_a", "p2", 1): 0, ("task_b", "p1", 1): 0}),
        ("right", {("task_a", "p1", 1): 1, ("task_a", "p2", 1): 1, ("task_b", "p1", 1): 0}),
    ):
        for (task_id, policy, repeat), value in values.items():
            rows.append(
                {
                    "condition": condition,
                    "task_id": task_id,
                    "response_policy": policy,
                    "repeat": repeat,
                    "result": {"metric": value},
                }
            )

    result = paired(rows, "left", "right", "metric", 100, 7)

    assert result["matched_case_repeat_pairs"] == 3
    assert result["task_clusters"] == 2
    assert result["cluster_weighting"] == "equal-weight task means"
    assert result["estimate"] == 0.5


def test_paired_estimator_handles_no_matches():
    result = paired([], "left", "right", "metric", 100, 7)
    assert result["estimate"] is None
    assert result["task_cluster_bootstrap_95"] is None


def test_clustered_rate_equal_weights_tasks_not_episodes():
    rows = [
        {"task_id": "task_a", "result": {"metric": value}}
        for value in (1, 1, 1)
    ] + [{"task_id": "task_b", "result": {"metric": 0}}]

    result = clustered_rate(rows, "metric", 100, 7)

    assert result["task_clusters"] == 2
    assert result["valid_episodes"] == 4
    assert result["estimate"] == 0.5


def test_clustered_rate_handles_undefined_metric():
    rows = [{"task_id": "task_a", "result": {"metric": None}}]
    result = clustered_rate(rows, "metric", 100, 7)
    assert result["estimate"] is None
    assert result["task_cluster_bootstrap_95"] is None
