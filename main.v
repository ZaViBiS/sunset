/*_- sunset -_*/
module main

import time
import x.json2
import net.http

import config
import garland

fn main() {
	println(config.art)
	mut point := true // Это чтобы включить только ондин раз
	mut sunset_time := get_the_time_anyway(config.today_url)
	for true {
		point = check_n_do(point, mut sunset_time)
		time.sleep(time.minute * 10) // 10 min time sleep
	}
}

fn check_n_do(point bool, mut sunset_time time.Time) bool {
	off_time := time.parse('${time.now().ymmdd()} 22:30:00') or { return point }

	if sunset_time < time.now() && point {
		garland.switch(true)
		sunset_time = get_the_time_anyway(config.tomorrow_url)
		return false
	} 
	if off_time < time.now() {
		garland.switch(false)
		return true
	}
	return point
}

fn get_sunset_time(url string) time.Time {
	resp := http.get(url) or {
		error := time.parse(config.error_time) or {exit(1)}
		return error
	}
	data := json2.raw_decode(resp.text) or {
		error := time.parse(config.error_time) or {exit(1)}
		return error
	}.as_map()

	no_parse := data['results'] or {
		println('error get_sunset_time1')
		return time.now()
		}.as_map()['sunset'] or {
			println('error get_sunset_time2')
			return time.now()
		}
	sunset_time := time.parse_iso8601(no_parse.str()) or {
		println('error get_sunset_time3')
		return time.now()
		}
	return sunset_time.add(time.seconds_per_hour * time.second * 2) // +2 hour
}

fn get_the_time_anyway(url string) time.Time {
	/* проверяет правильность полученого времени*/
	mut out_time :=  get_sunset_time(url)
	for _ in 0..10000 {
		if out_time.str() != config.error_time.str() {
			return out_time
		}
		out_time = get_sunset_time(url)
		time.sleep(time.second * 10) // 10 sec
	}
	return out_time
}
