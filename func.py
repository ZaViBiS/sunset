import datetime
import json
import time
import urllib.request

from config import blynk_url, url


def get_the_time_anyway(url: str) -> list:
    for _ in range(10000):
        out_time = get_time(url)
        if len(out_time) == 2:
            return out_time


def datetime_parse_ISO8601(data: str) -> datetime.datetime:
    # +2 часа чтобы учесть часово поялс
    # Мой +2 что очевидно
    return datetime.datetime.strptime(data[:-7], "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(hours=2)


def datetime_parse(data: str) -> datetime.datetime:
    return datetime.datetime.strptime(data, "%H:%M:%S")


def get_time(url: str) -> list:
    # По ссыке получает время заката и рассвета и возвращяет список
    # [Время заката, Время рассвета]
    resp = get(url)
    if not resp:
        return []
    data = json.loads(resp.read())['results']
    sunset_time = datetime_parse_ISO8601(data['sunset'])
    sunrise_time = datetime_parse_ISO8601(data['sunrise'])
    return [sunset_time, sunrise_time]


def check_n_do_sunset(timings: list):
    evning_off_time = datetime_from_stings('22:30:00')
    now = datetime.datetime.now()
    print(evning_off_time)
    if timings[0] < now and evning_off_time > now:
        print('sunset garland on')
        garland(True)
        time.sleep((evning_off_time - now).total_seconds())
        timings = get_the_time_anyway(url)
    if evning_off_time < now:
        print('sunset garland off')
        garland(False)
        time.sleep((now - timings[1]).total_seconds())


def check_n_do_sunrise(timings: list):
    morining_off_time = datetime_from_stings('9:00:00')
    now = datetime.datetime.now()
    if timings[1] < now and morining_off_time > now:
        garland(True)
        time.sleep((morining_off_time - now).total_seconds())
        timings = get_the_time_anyway(url)
    if morining_off_time < now:
        garland(False)
        time.sleep((now - morining_off_time).total_seconds())


def garland(do: bool) -> bool:
    # Включает или отключает герлянду
    if do:
        get(blynk_url+'1')
        return True
    else:
        get(blynk_url+'0')
        return False


def get(url: str) -> urllib.request.http.client.HTTPResponse:
    try:
        return urllib.request.urlopen(url)
    except:
        return False


def datetime_from_stings(data: str) -> datetime.datetime:
    # Семерки нужны чтобы из обрезали в функции datetime_parse_ISO8601
    # Зачем что-то обрезать?
    # Потому что получаемые данные идут с учетом часового пояса, а мне это не надо
    today = datetime.date.today()
    return datetime_parse_ISO8601(f'{today.strftime("%Y-%m-%d")}T{data}'+7*'7')
