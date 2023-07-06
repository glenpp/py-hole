# DNS Firewall (blackhole malicious, like Pi-hole) with bind9

A [Pi-hole](https://github.com/pi-hole/pi-hole) inspired DNS firewall / blackhole for use with bind/named using RPZ.

After listening to [Security Weekly #507](http://wiki.securityweekly.com/wiki/index.php/Episode507) where Malvertising and [Pi-hole](https://pi-hole.net/) was discussed, I wanted to try something similar that fitted the setup of my networks better. While blacklisting approaches have limited benefit, and should not be applied without the endpoint owner's consent (they can badly break stuff), this does none the less reduce exposure to malicious actors as well as allowing mitigation against accidental access to undesirable sites.

I was disappointed this relied on dnsmasq and wondered if it wouldn't be possible to the same with bind9. Fortunately it turned out to be rather easy thanks to RPZ available since bind 9.8, so this is how I did it....

## Maintaining RPZ zone file

This is essentially the blacklist, or Response Policy Zone (RPZ) file which tells bind what to do when it gets a query for a name or pattern we want to blackhole.

It took an hour or so to fish out a bunch of blacklist URLs from the Pi-hole source, figure out the formats and put together a Python script to maintain an RPZ zone file. The aim is that this will be able to understand multiple formats so as other sources become available we can update accordingly. It also caches files so that we don't have to keep re-fetching which is a pain while developing and testing.

From there I've built in a bunch of refinements including a config file, support for extra local blacklist entries, exclusions and other tricks.

## Stats

A useful feature of bind is that it has an XML via http monitoring/statistics interface that can be enabled This needs the following adding to the configuration (**/etc/bind/named.conf.options** on Debian/Ubuntu and derived distros) to enable the service:

```
statistics-channels {
    inet 127.0.0.1 port 5380 allow { 127.0.0.1; };
};
```

Where 5380 is the port it will listen on. Many examples use 8080 as the port, but since that's a popular one for proxies and application servers, I've opted for a different one to avoid conflicts.

If you make a request from **`http://127.0.0.1:5380/`** you will get an XML file of all the internal stats within bind.

Within that XML file there are a bunch of stats (follow the tags) that represent RPZ related counters:

- server.nsstat.RPZRewrites
- views._default.zones.zone.rcode.RPZRewrites for each zone
- views._default.zones.zone.rcode.\* for the RPZ zone

The problem I have is that apart from the first one, all of these seem to return 0 so I'm guessing only the first one is useful for monitoring.

I am working on Cacti templates for monitoring bind, but since the volume of stats is so large and there are significant differences between formats of minor versions, don't expect to see anything soon.

## Setup

To get this working you need the config file /etc/bind/py-hole-bind9RPZ_config.yaml which you can use the template to start off with. The options should be straight forward in the comments of the file. You need to ensure that the rpzfile, rpztemplate (provides the header to the zone file) and reloadzonecommand (list of arguments) match your configuration. The remainder are things you can tweak.

There are some source formats supported:

- **raw** - this is simply a list of hosts, one per line, and we assume lines starting with "#" are comments.
- **hosts** - this is the standard /etc/hosts format, and here we need a hostkey specifier to match the IP from the hosts file that blacklisted hosts use.
- **abp** - Adblock Plus format.
- **json** - JSON data with appropriate selectors.
- **rpz** - native format directly.

Once you have a config file then you can run the Python script. This will download the source lists to a cache location (specified in the config or defaulting to /var/local/bindRPZ) and process them into your output file specified by rpzfile in the config.

```
# ./py-hole-bind9RPZ
```

Check the output file is as you expect it to be, tweak the config and re-run as you need to get this working.

In particular, I would recommend that you review the blacklist sources since these could have impact on your network if they block useful hosts, or worse, if a malicious actor got control and was able to inject their own content.

When you're ready to start blocking, then edit the zones list (/etc/bind/named.conf.local on Debian/Ubuntu and derived distros) and add the zone matching your configuration:

```
zone "rpz.example.com" {
        type master;
        file "/etc/bind/db.rpz.example.com";
};
```

Then in the options section (/etc/bind/named.conf.options on Debian/Ubuntu and derived distros) add the RPZ configuration:

```
    response-policy {zone "rpz.example.com";};
```

Then reload bind, check the logs and you should have the domains in the list being blocked.

To disable this again, simply remove or comment what you added to the bind configuration and you can also delete the RPZ zone file, config, cache files etc.

To be able to run the script you will need the following packages (assuming Debian and derived distros):

- python3
- python3-yaml (PyYAML)
- python3-requests

For regular updates, put the Python script py-hole-bind9RPZ in an appropriate cron directory (eg. /etc/cron.weekly/) to keep the records up to date. When it runs it should automatically run your configured command to reload the zone after the update.

## Update 2020-07-17

I've been a bit quiet on this but in the background making a whole lot of updates that haven't gone into the public repo. These include:

- Safer downloading by dropping privilege in a forked process for the download (may help mitigate hostile servers attacking a vulnerable client)
- Sanity checking of downloaded content (max size, min size, per-line limits and regex check, freshness checks, etc.)
- More intelligent caching including checking with HEAD before performing a GET
- Managing multiple RPZ zones for different categories of blocklist (eg. be able to see in logs when a malware RPZ is hit vs an advertising RPZ which might provide some level of threat/compromise detection opportunities)
- Better logging and console output (more verbose automatically when run on the console).
- Retrying failed connections, going with the last cached file when we can't update..... within reason.
- Various bugfixes.
- Generally tidier, more mature code with things having had lots of refinement from the initial quick-n-dirty script.

**IMPORTANT:** With this update, the config file has also changed to accommodate the improvements. Some basic checks are done to see if the config file is in the old format, but these are not comprehensive. Take a look at the example config file before using these newer versions.

