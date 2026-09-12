import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('limit', [16, 64])
def test_capacity_wrapper_enforces_new_bound(limit):
    module = load('gateway_capacity')
    semaphore = module.ThreadingCapacity(limit).BoundedSemaphore(12)
    assert all(semaphore.acquire(blocking=False) for _ in range(limit))
    assert not semaphore.acquire(blocking=False)
    semaphore.release()
    assert semaphore.acquire(blocking=False)


def test_resume_preserves_failed_attempt_and_refuses_active_registration(tmp_path):
    module = load('schedule_api_capacity')
    job = dict(run_id='test', stage='main-v1', agent='codex', model='model', condition='neutral', repeat=1, case_id='case')
    folder = tmp_path / 'runs/main-v1/test'
    folder.mkdir(parents=True)
    result = dict(job, completed=False)
    (folder / 'attempt_status.json').write_text(json.dumps(result))
    assert module.completed_and_pending([job], tmp_path) == ([result], [])
    (folder / 'attempt_status.json').unlink()
    (tmp_path / 'registry').mkdir()
    (tmp_path / 'registry/test.json').write_text('{}')
    with pytest.raises(ValueError, match='drain first'):
        module.completed_and_pending([job], tmp_path)
