# import pystemd

# manager = pystemd.Manager()

# manager.Manager.ListUnitFiles()

from pystemd.systemd1 import Manager, Unit

manager = Manager()

manager.load()

result = manager.Manager.ListUnitFiles()

# print(result)

stopped = manager.Manager.StopUnit("cron.service", "replace")

print(stopped)

started = manager.Manager.StartUnit("cron.service", "replace")

print(started)
