"""Preserve native episodes and the ablation barrier with bounded capacity."""
from concurrent.futures import ThreadPoolExecutor, wait
import json
from pathlib import Path
import sys
import time

from hil_guard_v4 import launch as native
import sail_v4_capacity


class MainFirstPool(ThreadPoolExecutor):
    expected_main = 5760
    already_closed_main = 0
    checkpoint = None
    check_resources = staticmethod(native.ready)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_futures = []
        self.ablation_started = False

    def submit(self, fn, job, *args, **kwargs):
        ablation = job['condition'] == 'sail_v4_no_human'
        if ablation and not self.ablation_started:
            if len(self.main_futures) + self.already_closed_main != self.expected_main:
                raise ValueError('Ablation appeared before all planned main jobs were submitted')
            # Waiting does not retry or replace a failed future. The native
            # launcher records each result or failure after this barrier.
            wait(self.main_futures)
            while not self.check_resources():
                time.sleep(3)
            if self.checkpoint:
                native.save(self.checkpoint, {'main_workers_finished_unix':time.time(),
                    'main_attempts':self.expected_main,'ablation_may_start':True,
                    'analysis_status':'pending separate score collection and audit'})
            self.ablation_started = True
        if not ablation and self.ablation_started:
            raise ValueError('Main job found after the ablation barrier')
        future = super().submit(fn,job,*args,**kwargs)
        if not ablation:
            self.main_futures.append(future)
        return future


def main():
    # Episode execution is unchanged. The capacity amendment changes only
    # admission scheduling and records every capacity decision.
    plan_path = Path(sys.argv[1])
    plan = json.loads(plan_path.read_text())
    if plan.get('analysis_only') or plan.get('execution_order') != 'main_then_ablation':
        raise ValueError('A frozen main-then-ablation plan is required')
    main_jobs = [j for j in plan['jobs'] if j['condition'] != 'sail_v4_no_human']
    MainFirstPool.expected_main = len(main_jobs)
    MainFirstPool.already_closed_main = sum((native.ROOT/'runs'/j['stage']/j['run_id']/'attempt_status.json').exists() for j in main_jobs)
    checkpoint = ('sail4-main-completion.json' if plan['phase'] != 'preflight'
                  else plan['experiment'] + '-main-completion.json')
    MainFirstPool.checkpoint = native.ROOT/'reports'/checkpoint
    sail_v4_capacity.main(pool_type=MainFirstPool)


if __name__ == '__main__':
    main()
