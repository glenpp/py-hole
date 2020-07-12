# py-hole
A [Pi-hole](https://github.com/pi-hole/pi-hole) inspired DNS firewall / blacklister for use with bind/named using RPZ (plus Laptops running NetworkManager with dnsmasq)

For full details see https://www.pitt-pladdy.com/blog/_20170407-105402_0100\_DNS\_Firewall\_blackhole\_malicious\_like\_Pi-hole\_with\_bind9/

## Dependencies
This may vary by distro, but the ones given here are based on Debian and derived distros. The script is Python 3 as 2.x is now pretty old and heading towards retirement. Python 3 has had major modules ported and has been working well for some time now, so this project has moved over.

- python3
- python3-yaml (PyYAML)
- python3-requests

## py-hole-bind9RPZ & py-hole-bind9RPZ\_config.yaml
This updates a bind9 RPZ (Response Policy Zone) file against configuration in /etc/bind/py-hole-rpzconfig.yaml

## py-hole-dnsmasq & py-hole-dnsmasq\_config.yaml
These have gone away with this configuration not being common on laptops or other standalone devices for some time. Things have switched instead to systemd-resolved which isn't apparent how to implement something like this.

