#!/usr/bin/env python3
#
#  valentines_shrove_tuesday.py
"""
Calculate when Shrove Tuesday falls on the same day as Valentines Day.
"""
#
#  Copyright © 2026 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import datetime

# 3rd party
import matplotlib.dates
from domdf_python_tools.dates import calc_easter
from matplotlib import pyplot as plt

years = []
shrove_tuesday_dates = []
colours = []
coincide_years = []

start_year = 1900
end_year = 2100
this_year = datetime.date.today().year
leap_year = 2000

valentines_day = datetime.date(year=leap_year, month=2, day=14)
epoch = datetime.date(1970, 1, 1)

for year in range(start_year, end_year + 1):
	easter = calc_easter(year)
	shrove_tuesday = easter - datetime.timedelta(days=47)

	years.append(year)
	shrove_tuesday_dates.append(datetime.date(year=leap_year, month=shrove_tuesday.month, day=shrove_tuesday.day))

	if shrove_tuesday.month == valentines_day.month and shrove_tuesday.day == valentines_day.day:
		colours.append("red")
		coincide_years.append(year)
	elif year == this_year:
		colours.append("orange")
	else:
		colours.append("blue")


def get_normal_years(seq):
	return [x for x, y in zip(seq, years) if y not in coincide_years]


def get_matching_years(seq):
	return [x for x, y in zip(seq, years) if y in coincide_years]


plt.plot(years, shrove_tuesday_dates, clip_on=False)
# plt.scatter(years, shrove_tuesday_dates, c=colours, zorder=100, clip_on=False)

plt.scatter(
		get_normal_years(years),
		get_normal_years(shrove_tuesday_dates),
		c=get_normal_years(colours),
		zorder=100,
		clip_on=False,
		)

plt.scatter(
		get_matching_years(years),
		get_matching_years(shrove_tuesday_dates),
		c=get_matching_years(colours),
		marker=r"$♥$",
		s=plt.rcParams["lines.markersize"]**2 + 20,
		zorder=100,
		clip_on=False,
		)

plt.hlines([valentines_day], xmin=start_year, xmax=end_year, colors=["red"])

ax = plt.gca()
x_ticks = list(ax.get_xticks())
extra_x_ticks = coincide_years + [datetime.date.today().year]
x_ticks = [tick for tick in x_ticks if not any(abs(tick - year) < 2 for year in extra_x_ticks)]
ax.set_xticks(x_ticks + extra_x_ticks)

ax.set_xlim(start_year, end_year)

ax.yaxis.set_major_formatter(matplotlib.dates.DateFormatter("%d/%m"))

ax.set_yticks(list(ax.get_yticks()) + [float((valentines_day - epoch).days)])

plt.xlabel("Year")
plt.ylabel("Date")
plt.title("Dates of Shrove Tuesday versus Valentines Day")
plt.grid(True, which="both")
plt.show()
