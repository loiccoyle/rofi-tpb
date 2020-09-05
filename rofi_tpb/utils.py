from tpblite.models.torrents import Torrent


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

    Returns:
        formatted string.
    """
    return string.format(
        title=torrent.title.strip(),
        filesize=torrent.filesize,
        seeds=torrent.seeds,
        leeches=torrent.leeches,
        uploader=torrent.uploader,
        upload_date=torrent.upload_date,
        url=torrent.url,
        magnetlink=torrent.magnetlink,
    )
