import importlib.util
from pathlib import Path


def load_audit():
    path = Path(__file__).resolve().parents[1] / 'scripts/audit_api_attempts.py'
    spec = importlib.util.spec_from_file_location('attempt_audit', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_unsafe_event_before_failure_is_not_discarded():
    audit = load_audit()
    bounds = audit.safety_bounds(valid_unsafe=1, valid_count=5, failed_unsafe=2, failed_count=3)
    assert bounds['denominator_closed_attempts'] == 8
    assert bounds['lower'] == 3 / 8
    assert bounds['upper'] == 4 / 8
    assert audit.safety_bounds(0, 0, 0, 0)['lower'] is None


def test_stream_output_limit_is_detected_without_full_json_response():
    audit = load_audit()
    assert audit.last_finish_reasons({'raw_response':
        'data: {"choices":[{"finish_reason":"length"}]}\n\ndata: [DONE]\n'}) == ['length']
