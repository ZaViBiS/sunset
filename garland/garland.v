module garland

import net.http

import config

pub fn switch(do bool) bool {
	if do {
		http.get(config.blynk_url+'1') or {
			return false
		}
		return true
	}else {
		http.get(config.blynk_url+'0') or {
			return false
		}
		return true
	}
}
