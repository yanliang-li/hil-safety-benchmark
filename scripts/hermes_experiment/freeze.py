"""Freeze the fourth-framework extension without rewriting the three-framework plan."""
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]


def main():
    base_path = ROOT / 'experiments/api-multimodel-20260912/main-plan-v1.json'
    dest = ROOT / 'experiments/api-multimodel-20260912/hermes-plan-v1.json'
    if dest.exists():
        raise FileExistsError('Do not overwrite the Hermes plan')
    base = json.loads(base_path.read_text())
    evidence = json.loads((ROOT / 'reports/hermes-framework-preflight.json').read_text())
    good = {(r['model'], r['condition']) for r in evidence['attempts'] if r['completed']}
    models = ['deepseek-v4-flash', 'glm-5.2', 'qwen3.7-max']
    conditions = ['neutral', 'prompt_guard_v1']
    if good != {(m, c) for m in models for c in conditions}:
        raise ValueError('All Hermes model/condition preflights must complete first')
    replay_path = ROOT / 'reports/hermes-preflight-replay.json'
    replay = json.loads(replay_path.read_text())
    successful_ids = {r['run_id'] for r in evidence['attempts'] if r['completed']}
    if {r['run_id'] for r in replay if r['score_replay_equal']} != successful_ids:
        raise ValueError('Successful preflights require independent score replay')
    jobs = []
    for old in base['jobs']:
        if old['agent'] != 'codex':
            continue
        job = {k: old[k] for k in ['model', 'condition', 'case_id', 'task_id', 'repeat', 'timeout']}
        job.update(agent='hermes', stage='hermes-main-v1')
        digest = hashlib.sha256(json.dumps(job, sort_keys=True).encode()).hexdigest()[:20]
        job['run_id'] = 'hermes01_' + digest
        jobs.append(job)
    assert len(jobs) == 1440 and len({j['run_id'] for j in jobs}) == 1440
    sources = dict(base['source_sha256'])
    for p in (ROOT / 'scripts/hermes_experiment').glob('*.py'):
        sources[str(p.relative_to(ROOT))] = hashlib.sha256(p.read_bytes()).hexdigest()
    plan = {
        'schema_version': 1, 'experiment': 'fourth-framework-hermes-extension',
        'frozen_unix': time.time(),
        'original_plan_sha256': hashlib.sha256(base_path.read_bytes()).hexdigest(),
        'selection_basis': 'Owner requested Hermes; same models, cases, conditions and repeats as the original matrix. Compatibility preflights excluded from main outcomes.',
        'jobs': jobs, 'cases': base['cases'], 'case_count': 80, 'task_cluster_count': 20,
        'repeats': 3, 'conditions': conditions, 'models': models,
        'total_planned_runs': 1440, 'combined_planned_runs': 5760,
        'image': 'hil-api-hermes:20260912-v1',
        'image_id': subprocess.check_output(['docker', 'image', 'inspect', 'hil-api-hermes:20260912-v1', '--format', '{{.Id}}'], text=True).strip(),
        'upstream': {'repository': 'https://github.com/NousResearch/hermes-agent',
                     'commit': 'b7b35a84b7fbe1aa2e223a6ce726a2471300d0a4', 'version': '0.21.2'},
        'source_sha256': sources, 'protocol': 'chat_completions',
        'preflight_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in [ROOT / 'reports/hermes-framework-preflight.json', replay_path]},
        'tool_interface': 'Native Hermes tool_search/tool_describe/tool_call bridge to ten allowlisted benchmark MCP tools.',
        'auxiliary_requests': 'Native session-title generation remains enabled; relay request counts and usage include it. Agent-loop requests use max_tokens=4096; preflight title requests contain no explicit output-token limit.',
        'configured_context_length': 65536,
        'context_note': 'Hermes enforces a 64,000-token initialization floor. Its configured 65,536-token window differs from the 32,768 setting in Codex and DeepSeek Harness. Claude Code retains native context handling. These settings do not verify endpoint context limits.',
        'limits': {'total_agent_concurrency': 32, 'hermes_workers_while_other_frameworks_run': 8,
                   'other_framework_workers': 24, 'agent_memory_mib': 1536, 'agent_cpu': 1,
                   'timeout_seconds': 900, 'max_requests_per_attempt': 48},
        'scope': 'Reused exploratory pilot tasks; third-party model weights unverified. Hermes runs start later in calendar time; serving drift remains a possible confound.',
    }
    dest.write_text(json.dumps(plan, indent=2) + '\n')
    print(json.dumps({'plan': str(dest.relative_to(ROOT)), 'runs': len(jobs),
                      'sha256': hashlib.sha256(dest.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
