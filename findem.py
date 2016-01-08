#!/usr/bin/env python
import sys
import re
import os
import operator
from optparse import OptionParser

usage = "usage: %s: \"## ## ## ## ## ##\"\n" % os.path.basename(sys.argv[0])
usage += "Need string containing 6 numbers, 5 winners and a bonus"

payouts = {}

# From http://en.wikipedia.org/wiki/Mega_Millions
payouts['mega'] = {
	(5, True) : 500000000,
	(5, False) : 1000000,
	(4, True) : 10000,
	(4, False) : 100,
	(3, True) : 100,
	(2, True) : 7,
	(3, False) : 7,
	(1, True) : 4,
	(0, True) : 4,
}

# From http://www.powerball.com/powerball/pb_prizes.asp
payouts['powerball'] = {
	(5, True) : 500000000,
	(5, False) : 1000000,
	(4, True) : 50000,
	(4, False) : 100,
	(3, True) : 100,
	(2, True) : 7,
	(3, False) : 7,
	(1, True) : 4,
	(0, True) : 4,
}

def line_to_nums(line):
	set = None
	m = re.match("(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", line)
	if m:
		set = [ (int(m.group(1)), int(m.group(2)), int(m.group(3)),
			 int(m.group(4)), int(m.group(5))), int(m.group(6)) ]
	return set;

def find_winners(payouts, numbers, winners):
	payout = 0
	for set in numbers:
		count = 0
		for num in winners[0]:
			if num in set[0]:
				count += 1

		bonus = (winners[1] == set[1])

		if (count, bonus) in payouts:
			num = " ".join(map(str, set[0]))
			num += " %d" % set[1]
			print "  %s pays out $%d" % (num, payouts[(count, bonus)])
			payout += payouts[(count, bonus)]
	return payout


numbers = []
hist = {}
bhist = {}
for line in sys.stdin.readlines():
	set = line_to_nums(line)
	if set:
		for num in set[0]:
			if num in hist:
				hist[num] += 1
			else:
				hist[num] = 0
		if set[1] in bhist:
			bhist[set[1]] += 1
		else:
			bhist[set[1]] = 0
		numbers.append(set)


parser = OptionParser(usage=usage)
parser.add_option("-H", "--hist", action="store_true", default=False, help="Print histogram of lotto numbers")
parser.add_option("-m", "--mega", action="store_true", default=False, help="Use Mega Millions rules")
parser.add_option("-p", "--powerball", action="store_true", default=False, help="Use Powerball rules")

(options, args) = parser.parse_args()

if options.hist:
	sorted_nums = sorted(hist.iteritems(), key=operator.itemgetter(1),
			     reverse=True)
	sorted_bonus = sorted(bhist.iteritems(), key=operator.itemgetter(1),
			      reverse=True)

	print "5 most common regular numbers:"
	for nums in sorted_nums[:5]:
		print "  %.2d (%d)" % (nums[0], nums[1])

	print ""
	print "5 most common bonus numbers:"
	for nums in sorted_bonus[:5]:
		print "  %.2d (%d)" % (nums[0], nums[1])

if len(args) != 1 and not options.hist:
	parser.print_help()
	sys.exit(1)

rules = payouts['powerball']

if options.mega and options.powerball:
	print >>sys.stderr, "Can only use one of --mega or --powerball."
	parser.print_help()
	sys.exit(1)

if options.mega:
	rules = payouts['mega']
elif options.powerball:
	rules = payouts['powerball']

if len(args) == 1:
	winners = line_to_nums(args[0])
	if winners is not None:
		if options.hist:
			print ""
		print "--- PAYOUT ---"
		payout = find_winners(rules, numbers, winners)

		print ""
		print "Total payout: $%d" % payout
	else:
		parser.print_help()
		sys.exit(1)
