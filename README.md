# Automatic YouTube subtitle generation (A fork from https://github.com/m1guelpf/yt-whisper)

This repository uses `yt-dlp` and [OpenAI's Whisper](https://openai.com/blog/whisper) to generate subtitle files for any youtube video.

## Installation

To get started, you'll need Python 3.7 or newer. Install the binary by running the following command:

    pip uninstall yt-whisper -y
    pip install git+https://github.com/aichr/yt-whisper.git

Need to install [`ffmpeg`](https://ffmpeg.org/) first.

## Usage

```
# Transcribe a local video
yt_whisper ~/Downloads/awesome_video.mp4

# Transcribe a Youtube video (default using `small` model)
yt_whisper "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Transcribe a Youtube video using a better model (--model is one of `tiny`, `tiny.en`, `base`, `base.en`, `small`, `small.en`, `medium`, `medium.en`, `large`)
yt_whisper "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --model medium

# Adding `--task translate` will translate the subtitles into English:
yt_whisper "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --task translate

# Run the following to view all available options:
yt_whisper --help
```

## License

This script is open-source and licensed under the MIT License. For more details, check the [LICENSE](LICENSE) file.
