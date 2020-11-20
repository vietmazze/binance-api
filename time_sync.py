import time


def _get_time_offset(self):
    res = self.b.get_server_time()
    return res['serverTime'] - int(time.time() * 1000)


def synced(self, fn_name, **args):
    args['timestamp'] = int(time.time() - self.time_offset)
    return getattr(self.b, fn_name)(**args)
