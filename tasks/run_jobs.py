#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: run_jobs.py
@time: 2018-02-10 18:01
"""


from apscheduler.schedulers.blocking import BlockingScheduler

from config import current_config

from tasks import job_put_tasks
from tasks.jobs_sogou import job_sogou_cookies
from tasks.jobs_weixin import job_weixin_cookies
from apps.client_rk import counter_clear as job_counter_clear

REDIS = current_config.REDIS

scheduler = BlockingScheduler()

job_store_redis_alias = 'news_spider'


def add_job_store_redis():
    """
    127.0.0.1:6379> TYPE "example.jobs"
    hash
    127.0.0.1:6379> TYPE "example.run_times"
    zset
    127.0.0.1:6379> HGETALL "example.jobs"
    1) "45431465e6104f3c924ec01852ed1aeb"
    2) "\x80\x02}q\x01(U\x04argsq\x02)U\bexecutorq\x03U\adefaultq\x04U\rmax_instancesq\x05K\x01U\x04funcq\x06U\x10__main__:task_03q\aU\x02idq\bU 45431465e6104f3c924ec01852ed1aebq\tU\rnext_run_timeq\ncdatetime\ndatetime\nq\x0bU\n\a\xe1\x0c\b\x02\x01\x00\x00\x00\x00cpytz\n_p\nq\x0c(U\rAsia/Shanghaiq\rM\x80pK\x00U\x03CSTq\x0etRq\x0f\x86Rq\x10U\x04nameq\x11U\atask_03q\x12U\x12misfire_grace_timeq\x13K\x01U\atriggerq\x14capscheduler.triggers.cron\nCronTrigger\nq\x15)\x81q\x16}q\x17(U\btimezoneq\x18h\x0c(h\rM\xe8qK\x00U\x03LMTq\x19tRq\x1aU\aversionq\x1bK\x01U\nstart_dateq\x1cNU\bend_dateq\x1dNU\x06fieldsq\x1e]q\x1f(capscheduler.triggers.cron.fields\nBaseField\nq )\x81q!}q\"(U\nis_defaultq#\x88U\x0bexpressionsq$]q%capscheduler.triggers.cron.expressions\nAllExpression\nq&)\x81q'}q(U\x04stepq)Nsbah\x11U\x04yearq*ubh )\x81q+}q,(h#\x88h$]q-h&)\x81q.}q/h)Nsbah\x11U\x05monthq0ubcapscheduler.triggers.cron.fields\nDayOfMonthField\nq1)\x81q2}q3(h#\x88h$]q4h&)\x81q5}q6h)Nsbah\x11U\x03dayq7ubcapscheduler.triggers.cron.fields\nWeekField\nq8)\x81q9}q:(h#\x88h$]q;h&)\x81q<}q=h)Nsbah\x11U\x04weekq>ubcapscheduler.triggers.cron.fields\nDayOfWeekField\nq?)\x81q@}qA(h#\x88h$]qBh&)\x81qC}qDh)Nsbah\x11U\x0bday_of_weekqEubh )\x81qF}qG(h#\x89h$]qHcapscheduler.triggers.cron.expressions\nRangeExpression\nqI)\x81qJ}qK(h)NU\x04lastqLK\x16U\x05firstqMK\x00ubah\x11U\x04hourqNubh )\x81qO}qP(h#\x89h$]qQhI)\x81qR}qS(h)NhLK\x01hMK\x01ubah\x11U\x06minuteqTubh )\x81qU}qV(h#\x88h$]qWhI)\x81qX}qY(h)NhLK\x00hMK\x00ubah\x11U\x06secondqZubeubU\bcoalesceq[\x88h\x1bK\x01U\x06kwargsq\\}q]u."
    3) "f5637d98946848c291da09a4ceb08027"
    4) "\x80\x02}q\x01(U\x04argsq\x02)U\bexecutorq\x03U\adefaultq\x04U\rmax_instancesq\x05K\x01U\x04funcq\x06U\x10__main__:task_04q\aU\x02idq\bU f5637d98946848c291da09a4ceb08027q\tU\rnext_run_timeq\ncdatetime\ndatetime\nq\x0bU\n\a\xe1\x0c\b\x012\x00\x00\x00\x00cpytz\n_p\nq\x0c(U\rAsia/Shanghaiq\rM\x80pK\x00U\x03CSTq\x0etRq\x0f\x86Rq\x10U\x04nameq\x11U\atask_04q\x12U\x12misfire_grace_timeq\x13K\x01U\atriggerq\x14capscheduler.triggers.cron\nCronTrigger\nq\x15)\x81q\x16}q\x17(U\btimezoneq\x18h\x0c(h\rM\xe8qK\x00U\x03LMTq\x19tRq\x1aU\aversionq\x1bK\x01U\nstart_dateq\x1cNU\bend_dateq\x1dNU\x06fieldsq\x1e]q\x1f(capscheduler.triggers.cron.fields\nBaseField\nq )\x81q!}q\"(U\nis_defaultq#\x88U\x0bexpressionsq$]q%capscheduler.triggers.cron.expressions\nAllExpression\nq&)\x81q'}q(U\x04stepq)Nsbah\x11U\x04yearubh )\x81q*}q+(h#\x88h$]q,h&)\x81q-}q.h)Nsbah\x11U\x05monthubcapscheduler.triggers.cron.fields\nDayOfMonthField\nq/)\x81q0}q1(h#\x88h$]q2h&)\x81q3}q4h)Nsbah\x11U\x03dayubcapscheduler.triggers.cron.fields\nWeekField\nq5)\x81q6}q7(h#\x88h$]q8h&)\x81q9}q:h)Nsbah\x11U\x04weekubcapscheduler.triggers.cron.fields\nDayOfWeekField\nq;)\x81q<}q=(h#\x88h$]q>h&)\x81q?}q@h)Nsbah\x11U\x0bday_of_weekubh )\x81qA}qB(h#\x89h$]qCcapscheduler.triggers.cron.expressions\nRangeExpression\nqD)\x81qE}qF(h)NU\x04lastqGK\x16U\x05firstqHK\x00ubah\x11U\x04hourubh )\x81qI}qJ(h#\x89h$]qKh&)\x81qL}qMh)K\x01sbah\x11U\x06minuteubh )\x81qN}qO(h#\x88h$]qPhD)\x81qQ}qR(h)NhGK\x00hHK\x00ubah\x11U\x06secondubeubU\bcoalesceqS\x88h\x1bK\x01U\x06kwargsqT}qUu."
    5) "ba044f7b253a4cb1961e7abf036f8ef7"
    6) "\x80\x02}q\x01(U\x04argsq\x02)U\bexecutorq\x03U\adefaultq\x04U\rmax_instancesq\x05K\x01U\x04funcq\x06U\x10__main__:task_02q\aU\x02idq\bU ba044f7b253a4cb1961e7abf036f8ef7q\tU\rnext_run_timeq\ncdatetime\ndatetime\nq\x0bU\n\a\xe1\x0c\b\x012\r\x0f5\xf9cpytz\n_p\nq\x0c(U\rAsia/Shanghaiq\rM\x80pK\x00U\x03CSTq\x0etRq\x0f\x86Rq\x10U\x04nameq\x11U\atask_02q\x12U\x12misfire_grace_timeq\x13K\x01U\atriggerq\x14capscheduler.triggers.interval\nIntervalTrigger\nq\x15)\x81q\x16}q\x17(U\btimezoneq\x18h\x0c(h\rM\xe8qK\x00U\x03LMTq\x19tRq\x1aU\aversionq\x1bK\x01U\nstart_dateq\x1ch\x0bU\n\a\xe1\x0c\b\x01.\r\x0f5\xf9h\x0f\x86Rq\x1dU\bend_dateq\x1eNU\bintervalq\x1fcdatetime\ntimedelta\nq K\x00K<K\x00\x87Rq!ubU\bcoalesceq\"\x88h\x1bK\x01U\x06kwargsq#}q$u."
    127.0.0.1:6379> ZCARD "example.run_times"
    (integer) 3
    127.0.0.1:6379> ZRANGE "example.run_times" 0 2 WITHSCORES
    1) "f5637d98946848c291da09a4ceb08027"
    2) "1512669060"
    3) "ba044f7b253a4cb1961e7abf036f8ef7"
    4) "1512669073.9968569"
    5) "45431465e6104f3c924ec01852ed1aeb"
    6) "1512669660"

    # 清理数据
    127.0.0.1:6379> DEL example.jobs
    (integer) 1
    127.0.0.1:6379> DEL example.run_times
    (integer) 1
    :return:
    """
    scheduler.add_jobstore(
        'redis',
        alias=job_store_redis_alias,
        jobs_key='news_spider.jobs',
        run_times_key='news_spider.run_times',
        **REDIS
    )


def add_job():
    # sogou 反爬任务
    scheduler.add_job(
        job_sogou_cookies,
        'interval',
        kwargs={'spider_name': 'weixin'},
        minutes=5,
        id='job_sogou_cookies',
        replace_existing=True
    )

    # weixin 反爬任务
    scheduler.add_job(
        job_weixin_cookies,
        'interval',
        kwargs={'spider_name': 'weixin'},
        minutes=2,
        id='job_weixin_cookies',
        replace_existing=True
    )

    # 分布式任务调度 - 微信
    scheduler.add_job(
        job_put_tasks,
        'interval',
        kwargs={'spider_name': 'weixin'},
        minutes=5,
        id='job_put_tasks_weixin',
        replace_existing=True
    )

    # 分布式任务调度 - 微博
    scheduler.add_job(
        job_put_tasks,
        'interval',
        kwargs={'spider_name': 'weibo'},
        minutes=5,
        id='job_put_tasks_weibo',
        replace_existing=True
    )

    # 分布式任务调度 - 头条
    scheduler.add_job(
        job_put_tasks,
        'interval',
        kwargs={'spider_name': 'toutiao'},
        minutes=5,
        id='job_put_tasks_toutiao',
        replace_existing=True
    )

    # 计数清零
    scheduler.add_job(
        job_counter_clear,
        'cron',
        day='*',
        hour='0',
        id='job_counter_clear',
        replace_existing=True
    )


def run_blocking():
    try:
        # add_job_store_redis()   # 后端存储 基于redis(可选)
        add_job()               # 添加任务
        scheduler.start()       # 开启调度
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()    # 关闭调度


if __name__ == '__main__':
    run_blocking()
