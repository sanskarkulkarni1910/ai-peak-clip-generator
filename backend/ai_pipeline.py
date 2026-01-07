from backend.transcriber import transcribe_video


def collect_scores(peaks):
    return sorted(peaks, key=lambda x: x.get("score", 0), reverse=True)


def get_captions_for_video(video_path, clips):
    words = transcribe_video(video_path)

    for clip in clips:
        start = clip.get("start")

        # 🔥 MAIN FIX — end missing safe handling
        end = clip.get("end", start + 10)

        clip["end"] = end
        clip["caption"] = extract_caption(words, start, end)

    return clips


def extract_caption(words, start, end):
    text = []
    for w in words:
        if w.get("start") >= start and w.get("end") <= end:
            text.append(w.get("word", ""))
    return " ".join(text)
