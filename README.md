# py-hole
A [Pi-hole](https://github.com/pi-hole/pi-hole) inspired DNS firewall / blacklister for use with bind/named using RPZ (Response Policy Zone)

For full details see https://www.pitt-pladdy.com/blog/_20170407-105402_0100\_DNS\_Firewall\_blackhole\_malicious\_like\_Pi-hole\_with\_bind9/

## Dependencies
This may vary by distro, but the ones given here are based on Debian and derived distros. The script is Python 3 as 2.x is now pretty old and heading towards retirement. Python 3 has had major modules ported and has been working well for some time now, so this project has moved over.

- python3
- python3-yaml (PyYAML)
- python3-requests


## Install

- Copy py-hole-bind9RPZ_config.yaml to /etc/bind/ and adjust.
- Start the script `py-hole-bind9RPZ`
- Review the created zonefiles.

- Add config to `/etc/bind/named.conf.options`, inside the `options` section:
```
response-policy {
	zone "rpz.example.com";
	zone "rpz-malicious.example.com";
};
```

- Add config to `/etc/bind/named.conf.local`
```
zone "rpz.example.com" {
  type master;

  // py-hole
  file "/etc/bind/db.rpz.example.com";
};

zone "rpz-malicious.example.com" {
  type master;

  // py-hole
  file "/etc/bind/db.rpz-malicious.example.com";
};
```
