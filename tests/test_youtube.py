from video_tools import youtube


def test_build_options(tmp_path):
    cookies = tmp_path / "cookies.txt"
    cookies.write_text("test", encoding="utf-8")

    opts = youtube.build_yt_dlp_options(
        output_dir=tmp_path,
        video_format="best",
        resume=False,
        rate_limit="2M",
        cookies=cookies,
        retries=5,
    )

    assert opts["format"] == "best"
    assert opts["continuedl"] is False
    assert opts["ratelimit"] == "2M"
    assert opts["cookiefile"].endswith("cookies.txt")
    assert "%(uploader)s" in opts["outtmpl"]
