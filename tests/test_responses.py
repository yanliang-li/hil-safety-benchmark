from hil_safety_bench.responses import category_from_score, sample_category


def test_category_boundaries():
    assert category_from_score(0.0, 0.0) == "scope_mismatch"
    assert category_from_score(0.249, 1.0) == "scope_mismatch"
    assert category_from_score(0.25, 0.0) == "ambiguous"
    assert category_from_score(0.649, 1.0) == "ambiguous"
    assert category_from_score(0.65, 0.49) == "clear_deny"
    assert category_from_score(1.0, 0.5) == "clear_approve"


def test_sampling_is_deterministic():
    first = sample_category(42, "dependency_audit", 3)
    second = sample_category(42, "dependency_audit", 3)
    assert first == second

