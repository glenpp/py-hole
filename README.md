# py-hole
A [Pi-hole](https://github.com/pi-hole/pi-hole) inspired DNS firewall / blacklister for use with bind/named using RPZ (plus Laptops running NetworkManger with dnsmasq)

For full details see https://www.pitt-pladdy.com/blog/_20170407-105402_0100_DNS_Firewall_blackhole_malicious_like_Pi-hole_with_bind9/

## py-hole-bind9RPZ & py-hole-bind9RPZ_config.yaml
This updates a bind9 RPZ (Response Policy Zone) file against configuration in /etc/bind/py-hole-rpzconfig.yaml

## py-hole-dnsmasq & py-hole-dnsmasq_config.yaml
This is a variant designed for use on Laptops (and other roaming devices) running Mint or Ubuntu that use dnsmasq with NetworkManager.

Since these devices roam, they need local protection as we can't depend on whatever network they are connecting to.

Default config is coded in, but can be overridden with /etc/py-hole-config.yaml

