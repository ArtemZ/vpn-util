#
# Regular cron jobs for the vpn-util package
#
0 4	* * *	root	[ -x /usr/bin/vpn-util_maintenance ] && /usr/bin/vpn-util_maintenance
