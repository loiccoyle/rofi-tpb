# rofi-tpb
<p align="center">
  <img src="https://i.imgur.com/oBO2IFe.png">
</p>

<p align="center">
  <a href="https://github.com/loiccoyle/rofi-tpb/actions?query=workflow%3Atests"><img src="https://github.com/loiccoyle/rofi-tpb/workflows/tests/badge.svg"></a>
  <a href="./LICENSE.md"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="https://pypi.org/project/rofi-tpb/"><img src="https://img.shields.io/pypi/v/rofi-tpb"></a>
  <img src="https://img.shields.io/badge/platform-linux%20%7C%20macOS%7C%20windows-informational">
</p>

Dynamic menu interface for The Pirate Bay, built with [`rofi`](https://github.com/davatorium/rofi) in mind.

# Install

```shell
pip install rofi-tpb
```

Consider using [`pipx`](https://github.com/pipxproject/pipx):
```shell
pipx install rofi-tpb
```

# Usage

Prompt to either search tpb or browse tpb's top torrents:
```shell
rofi-tpb
```

Prompt for search query:
```shell
rofi-tpb search
```

Search for ubuntu related torrents:
```shell
rofi-tpb search ubuntu
```

Browse tpb's top torrents across all categories:
```shell
rofi-tpb top all
```

Browse tpb's recent top torrents across all categories in the last 48h:
```shell
rofi-tpb top all -r
```

Check the help for details:
```shell
rofi-tpb --help
...
rofi-tpb search --help
...
rofi-tpb top --help
...
```

# Dependencies

* `python >= 3.6`
* `tpblite`
* `dynmen`
* `lxml`
* `traitlets` (undeclared dependency of `dynmen`)


# Configuration

`rofi-tpb` stores its config in `$XDG_CONFIG_HOME/rofi-tpb/config.ini`.

The default configuration is the following:

```ini
[menu]
command = rofi -dmenu -i
torrent_format = {title:<65} 📁{filesize:<12} 🔽{seeds:<4} 🔼{leeches:<4} Trusted: {trusted} VIP: {vip}
vip_str = ✅
not_vip_str = ❌
trusted_str = ✅
not_trusted_str = ❌
use_tpb_proxy = True
tpb_url = https://thepiratebay0.org
categories = All, APPLICATIONS, AUDIO, GAMES, OTHER, PORN, VIDEO
categories_48h = True

[actions]
add = xdg-open '{magnetlink}'
open = xdg-open '{url}'
```

 * `menu.command`: the dynamic menu command which should read from `stdin` and output to `stdout`, if you want to use `dmenu` instead of `rofi` then adjust this command accordingly.
 * `menu.torrent_format`: text representation of a torrent in the dynamic menu, **accepts torrent string format keys.**
 * `menu.use_tpb_proxy`: if True will use the first tpb url as found on https://piratebayproxy.info/.
 * `menu.vip_str`: string to use in the `menu.torrent_format` when the user is VIP.
 * `menu.not_vip_str`: string to use in the `menu.torrent_format` when the user is not VIP.
 * `menu.trusted_str`: string to use in the `menu.torrent_format` when the user is trusted.
 * `menu.not_trusted_str`: string to use in the `menu.torrent_format` when the user is not trusted.
 * `menu.tpb_url`: tpb url, if `use_tpb_proxy` is True acts as a fallback url in case https://piratebayproxy.info/ is unavailable or the parsing fails.
 * `menu.categories`: comma separated list of tpb categories, when browsing the top torrents.
 * `menu.categories_48h`: add last 48h top torrent categories.
 * `actions.*`: commands to run on the selected torrent, **accepts torrent string format keys.**

Available torrent string format keys:
 * `{title}`: torrent title
 * `{filesize}`: torrent file size
 * `{seeds}`: number of seeders
 * `{leeches}`: number of leechers
 * `{uploader}`: torrent uploader
 * `{upload_date}`: upload date
 * `{url}`: torrent's tpb url
 * `{magnetlink}`: torrent magnet link
 * `{vip}`: uploader is VIP, replaced with `menu.vip_str`/`menu.not_vip_str`.
 * `{trusted}`: uploader is trusted, replaced with `menu.trusted_str`/`menu.not_trusted_str`.


If the `menu.command` uses `rofi`, `rofi-tpb` will use `rofi`'s `-multiple-select` flag to allow for selecting multiple torrents.
