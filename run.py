#!/usr/bin/env python3
# Author: Armit
# Create Time: 2022/10/11 

import os
import subprocess
from time import sleep
from datetime import datetime
from traceback import print_exc

# NOTE: This is DEPRECATED, do not use !!
# it seems impossible to accurately track process PID on Windows
# I tried TASKLIST, Powershell, subprocess.Popen, neither of them can get the correct PID :(


WEBUI_CMD = 'start /D sd-webui webui.bat'
NGROK_CMD = 'start ngrok.exe http 7860'
CHECK_INTERVAL = 10

TMP_PATH = os.environ['TMP']

SCEDULED_RESTART_AT = [
  ( 4, 0, 0),    # A.M. 04:00:00
  (12, 0, 0),    # P.M. 12:00:00
  (19, 0, 0),    # P.M. 19:00:00
]


def taskkill(pid) -> str:
  cmd = f'TASKKILL /PID /T {pid}'
  r = os.popen(cmd).read().strip()
  return r

def pid_exists(pid) -> bool:
  cmd = f'TASKLIST /FI "PID eq {pid}"'
  r = os.popen(cmd).read().strip()
  return 'No tasks are running' not in r

def clock_to_sec(h, m, s) -> int:
  return h * 60 * 60 + m * 60 + s


class SingletonPorcess:

  def __init__(self, name:str, cmd:str):
    self.name = name
    self.cmd = cmd
    self.pid = None
    self.pid_fp = os.path.join(TMP_PATH, f'{name}.pid')
    
    self.is_restarting = False

  def start(self):
    # check running
    if os.path.exists(self.pid_fp):
      try:
        with open(self.pid_fp, encoding='utf-8') as fh:
          pid = int(fh.read().strip())
      except:
        pid = None
      if pid and pid_exists(pid):
        if os.environ['IGNORE_LOCKFILE'] != 'true':
          print(f'The service {self.name} is already running at pid = {pid}!')
          print(f'If this is a mistake, manaully remove the lock file {self.pid_fp!r} and start again :)')
          print(f'or start with envvar IGNORE_LOCKFILE=true')
          exit(-1)

    # start new
    proc = subprocess.Popen(self.cmd)
    self.pid = proc.pid
    with open(self.pid_fp, 'w', encoding='utf-8') as fh:
      fh.write(str(self.pid))
    print(f'The service {self.name} is now running at pid = {self.pid}')

  def stop(self):
    # kill running
    while self.is_alive():
      taskkill(self.pid)
      sleep(3)

    if os.path.exists(self.pid_fp):
      os.unlink(self.pid_fp)

  def restart(self):
    if self.is_restarting: return

    self.is_restarting = True
    self.stop()
    sleep(1)
    self.start()
    sleep(1)
    self.is_restarting = False

  def is_alive(self) -> bool:
    if self.is_restarting: return

    pid_exists(self.pid)


if __name__ == '__main__':
  # monitor worker processes
  webui = SingletonPorcess('webui', WEBUI_CMD) ; webui.start()
  ngrok = SingletonPorcess('ngrok', NGROK_CMD) ; ngrok.start()
  sleep(3 * CHECK_INTERVAL)

  # begin daemon
  try:
    while True:
      # schedule
      flag = False
      now = datetime.now()
      now_s = clock_to_sec(now.hour, now.minute, now.second)
      for sched_tm in SCEDULED_RESTART_AT:
        sched_s = clock_to_sec(sched_tm[0], sched_tm[1], sched_tm[2])

        if abs(now_s - sched_s) < CHECK_INTERVAL / 2:
          print(f'Begin scheduled restart at {sched_tm}...')
          ngrok.stop()
          webui.restart()
          ngrok.start()
          sleep(2 * CHECK_INTERVAL)
          flag = True

      # normal check alive
      if not flag:
        if not webui.is_alive():
          print('The service webui is dead, try restarting...')
          webui.restart()
        if not ngrok.is_alive():
          print('The service ngrok is dead, try restarting...')
          ngrok.restart()
      
      # sleep
      sleep(CHECK_INTERVAL)
  except KeyboardInterrupt:
    print('Exit by Ctrl+C')
  except Exception:
    print_exc()
  finally:
    ngrok.stop()
    webui.stop()
