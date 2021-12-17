import time

import config
import func

print(config.art)
timings = func.get_the_time_anyway(config.url)
print(f'sunset time: {timings[0]}')
print(f'sunrise time: {timings[1]}')
while True:
    func.check_n_do_sunset(timings)
    func.check_n_do_sunrise(timings)
    time.sleep(1)
