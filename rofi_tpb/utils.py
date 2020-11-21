from tpblite.models.torrents import Torrent

from .config import CONFIG


def torrent_format(string: str, torrent: Torrent) -> str:
    """Format a torrent into a string.

    Args:
        string: string describing the format.
            Possible format keys:
                title: torrent.title
                filesize: torrent.filesize
                seeds: torrent.leeches
                leeches: torrent.leeches
                uploader: torrent.uploader
                upload_date: torrent.upload_date
                url: torrent.url
                magnetlink: torrent.magnetlink
                vip: uploader is vip
                trusted: uploader is trusted

    Returns:
        formatted string.
    """
    if torrent.is_vip:
        vip_str = CONFIG["menu"]["vip_str"]
    else:
        vip_str = CONFIG["menu"]["not_vip_str"]

    if torrent.is_trusted:
        trusted_str = CONFIG["menu"]["trusted_str"]
    else:
        trusted_str = CONFIG["menu"]["not_trusted_str"]

    return string.format(
        title=torrent.title.strip(),
        filesize=torrent.filesize,
        seeds=torrent.seeds,
        leeches=torrent.leeches,
        uploader=torrent.uploader,
        upload_date=torrent.upload_date,
        url=torrent.url,
        magnetlink=torrent.magnetlink,
        vip=vip_str,
        trusted=trusted_str,
    )
