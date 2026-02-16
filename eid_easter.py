# stdlib
import datetime

# 3rd party
import matplotlib.pyplot as plt
from domdf_python_tools.dates import calc_easter
from hijri_converter import Gregorian, Hijri


def calc_easter_eastern(year: int) -> datetime.date:
	"""
	Returns the date of Easter in the given year.

	:param year:
	"""

	a = year % 4
	b = year % 7
	c = year % 19
	d = ((19 * c) + 15) % 30
	e = ((2 * a) + (4 * b) - d + 34) % 7
	month = (d + e + 114) // 31
	day = ((d + e + 114) % 31) + 1

	return datetime.date(year, month, day) + datetime.timedelta(days=13)

deltas = {}  # Islamic year to days since easter that year

for islamic_year in range(1343, 1501):
	eid_date_hijri = Hijri(islamic_year, 10, 1)
	eid_date_gregorian = eid_date_hijri.to_gregorian()

	print("Eid:", eid_date_gregorian)

	gregorian_year = eid_date_gregorian.year
	easter_date_gregorian = calc_easter(gregorian_year)
	print("Easter:", easter_date_gregorian)

	delta = (eid_date_gregorian - easter_date_gregorian).days
	print("Delta:", delta, "days after Easter")
	print()

	deltas[islamic_year] = delta

fig = plt.figure(figsize=(8, 4))
plt.plot(list(deltas.keys()), list(deltas.values()))
plt.title("Number of days later Eid al-Fitr occurs in the Islamic year than Easter")
plt.xlabel(f"Islamic Year ({current_gregorian_year} AD = {current_islamic_year} AH)")
plt.ylabel("Days difference (-ve = before Easter)")
plt.xlim(1340, 1500)
plt.tight_layout()
plt.savefig("eid_easter.png")
plt.minorticks_on()
plt.grid(True, "both")
plt.show()
