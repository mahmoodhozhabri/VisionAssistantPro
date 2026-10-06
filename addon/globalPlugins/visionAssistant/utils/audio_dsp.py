# -*- coding: utf-8 -*-
import array


def _to_mono(samples, channels):
	if channels > 1:
		return samples[0::channels]
	return samples


def _resample(samples, src_rate, dst_rate):
	n_in = len(samples)
	if n_in < 2 or src_rate <= 0 or dst_rate <= 0 or src_rate == dst_rate:
		return samples
	n_out = int(n_in * dst_rate / src_rate)
	if n_out <= 0:
		return array.array("h")
	out = array.array("h", bytes(n_out * 2))
	if src_rate % dst_rate == 0:
		factor = src_rate // dst_rate
		for i in range(n_out):
			start = i * factor
			total = 0
			for j in range(factor):
				idx = start + j
				if idx < n_in:
					total += samples[idx]
			out[i] = int(total / factor)
		return out
	ratio = (n_in - 1) / max(1, n_out - 1)
	pos = 0.0
	for i in range(n_out):
		i0 = int(pos)
		if i0 >= n_in:
			i0 = n_in - 1
		frac = pos - i0
		s0 = samples[i0]
		s1 = samples[i0 + 1] if i0 + 1 < n_in else s0
		out[i] = int(s0 + (s1 - s0) * frac)
		pos += ratio
	return out