import json
import datetime
import os
import traceback
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from tqdm import trange

from a_databasetool.redis_tool import RedisQueue, RedisDctn
from utility.decorator_tools import show_process_and_thread_id
from utility.watch import Watch


class RedisTaskQueueManager:

    def __init__(self, fctn, redis_master):
        self.fctn = fctn
        self.redis_master = redis_master
        self.fctn_key_waiting = f'temp:TaskQueue:{fctn.__name__}:waiting'
        self.fctn_key_executing = f'temp:TaskQueue:{fctn.__name__}:executing'
        self.fctn_key_error = f'temp:TaskQueue:{fctn.__name__}:error'

        self.redisqueue_waiting = RedisQueue(name=self.fctn_key_waiting, redis_master=self.redis_master)
        self.redisdctn_executing = RedisDctn(name=self.fctn_key_executing, redis_master=self.redis_master)
        self.redisdctn_error = RedisDctn(name=self.fctn_key_error, redis_master=self.redis_master)

    def reset(self):
        self.redisqueue_waiting.delete()
        self.redisdctn_executing.delete()
        self.redisdctn_error.delete()
        print(f"reset {self.redisqueue_waiting.__class__.__name__} {self.redisqueue_waiting.name}")
        print(f"reset {self.redisqueue_waiting.__class__.__name__} {self.redisdctn_executing.name}")
        print(f"reset {self.redisqueue_waiting.__class__.__name__} {self.redisdctn_error.name}")

    def push_waiting(self, argskwargs_s):
        argskwargs_sent_s = [json.dumps(argskwargs) for argskwargs in argskwargs_s]
        self.redisqueue_waiting.push(argskwargs_sent_s)
        print(f"push {len(argskwargs_s)} items to {self.redisqueue_waiting.__class__.__name__} {self.redisqueue_waiting.name}")

    def batch_execute(self, ongoing=False):

        while True:
            pre_N = len(self.redisqueue_waiting)

            if pre_N > 0:
                w = Watch()
                while pre_N > 0:
                    # pop from waiting to executing
                    argskwargs_sent_s = self.redisqueue_waiting.pop()

                    for argskwargs_sent in argskwargs_sent_s:
                        self.redisdctn_executing[argskwargs_sent] = f'{datetime.datetime.now()}'
                        argskwargs = json.loads(argskwargs_sent)
                        try:
                            show_process_and_thread_id(self.fctn)(*argskwargs.get('args', []), **argskwargs.get('kwargs', {}))
                            print(f"SUCCESS {self.fctn.__name__} {argskwargs}", end='\t')
                        except Exception as e:
                            print(traceback.format_exc())
                            self.redisdctn_error[argskwargs_sent] = f'{datetime.datetime.now()}'
                            print(f"ERROR {self.fctn.__name__} {argskwargs}", end='\t')
                            # seconds = 60 * 1
                            # print(f"SLEEP {seconds} secs ......")
                            #
                            # for _ in trange(seconds, desc="Sleeping", unit="sec"):
                            #     time.sleep(1)

                        finally:

                            cur_N = len(self.redisqueue_waiting)
                            cost_single = w.see_timedelta()

                            finished_N = pre_N - cur_N
                            cost_multi = cost_single / finished_N if finished_N > 0 else pd.Timedelta('NaT')
                            estimate = cost_multi * cur_N

                            print(f'cost {round(cost_single.total_seconds(), 4)}/{finished_N} = {round(cost_multi.total_seconds(), 4)} remain {cur_N} estimate {estimate}')

                            pre_N = cur_N

                            del self.redisdctn_executing[argskwargs_sent]

                print('TASK DONE !')
                print(f"total cost {w.total_timedelta()}")
            else:
                if not ongoing:
                    break
                else:
                    pass
                    seconds = 60
                    print(f'SLEEP AT {datetime.datetime.now()}')
                    print(f"SLEEP {seconds} secs ......")

                    for _ in trange(seconds, desc="Sleeping", unit="sec"):
                        time.sleep(1)

    def check_done_block(self, check_interval=5):
        """
            使用单次调用 check_done 获取结果并处理
            """

        watch = Watch()
        prev_remaining = len(self.redisqueue_waiting)

        while prev_remaining > 0:
            cur_remaining = len(self.redisqueue_waiting)

            processed_items_cost = watch.see_timedelta()
            processed_items_num = prev_remaining - cur_remaining

            per_item_cost = processed_items_cost / processed_items_num if processed_items_num > 0 else np.inf

            remain_item_cost_est = per_item_cost * cur_remaining

            per_item_cost_seconds = round(per_item_cost.total_seconds(), 3) if per_item_cost != np.inf else np.inf
            processed_items_cost = round(processed_items_cost.total_seconds(), 3)

            print(f'{self.fctn.__name__} cost {processed_items_cost}/{processed_items_num} = {per_item_cost_seconds} sec/item, remain {cur_remaining} items, estimate {remain_item_cost_est}')

            prev_remaining = cur_remaining

            time.sleep(check_interval)

        while len(self.redisdctn_executing) > 0:
            time.sleep(0.01)

        print(f'{self.fctn.__name__} done!')

    def batch_execute_multiprocess(self, worker=os.cpu_count() - 1):
        # it will stuck in pychamr console so try to avoid using it.
        with ProcessPoolExecutor(max_workers=worker) as executor:
            for _ in range(worker):
                executor.submit(self.batch_execute)

    def restore_executing(self):
        argskwargs_sent_s = (self.redisdctn_executing.keys())
        self.redisqueue_waiting.push(argskwargs_sent_s)
        self.redisdctn_executing.delete()

    def restore_error(self):
        argskwargs_sent_s = (self.redisdctn_error.keys())
        self.redisqueue_waiting.push(argskwargs_sent_s)
        self.redisdctn_error.delete()


if __name__ == '__main__':
    pass
