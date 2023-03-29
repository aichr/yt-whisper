import os
import whisper
import time
from whisper.tokenizer import LANGUAGES, TO_LANGUAGE_CODE
import argparse
import warnings
import yt_dlp
from .utils import str2bool, slugify, write_vtt, write_srt, \
    write_txt, convert_video_to_audio_ffmpeg
import tempfile


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("video", nargs="+", type=str,
                        help="video URLs or a local path to transcribe")
    parser.add_argument("--model", default="small",
                        choices=whisper.available_models(),
                        help="name of the Whisper model to use")
    parser.add_argument(
        "--format", default="srt", choices=["vtt", "srt", "txt"],
        help="the subtitle format to output")
    parser.add_argument("--output_dir", "-o", type=str,
                        default=".", help="directory to save the outputs")
    parser.add_argument(
        "--verbose", type=str2bool, default=False,
        help="Whether to print out the progress and debug messages")
    parser.add_argument(
        "--task", type=str, default="transcribe",
        choices=["transcribe", "translate"],
        help="whether to perform X->X speech recognition ('transcribe') or X->English translation ('translate')")
    parser.add_argument("--language", type=str, default=None,
                        choices=sorted(LANGUAGES.keys()) +
                        sorted([k.title() for k in TO_LANGUAGE_CODE.keys()]),
                        help="language spoken in the audio, skip to perform language detection")

    parser.add_argument(
        "--break-lines", type=int, default=0,
        help="Whether to break lines into a bottom-heavy pyramid shape if line length exceeds N characters. 0 disables line breaking.")

    args = parser.parse_args().__dict__
    model_name: str = args.pop("model")
    output_dir: str = args.pop("output_dir")
    subtitles_format: str = args.pop("format")
    os.makedirs(output_dir, exist_ok=True)

    if model_name.endswith(".en"):
        warnings.warn(
            f"{model_name} is an English-only model, forcing English detection.")
        args["language"] = "en"

    model = whisper.load_model(model_name)
    audios = get_audio(args.pop("video"))
    break_lines = args.pop("break_lines")

    for title, audio_path in audios.items():
        warnings.filterwarnings("ignore")
        result = model.transcribe(audio_path, **args)
        warnings.filterwarnings("default")

        if subtitles_format == 'vtt':
            vtt_path = os.path.join(output_dir, f"{slugify(title)}.vtt")
            with open(vtt_path, 'w', encoding="utf-8") as vtt:
                write_vtt(result["segments"], file=vtt,
                          line_length=break_lines)

            print("Saved VTT to", os.path.abspath(vtt_path))
        elif subtitles_format == "srt":
            srt_path = os.path.join(output_dir, f"{slugify(title)}.srt")
            with open(srt_path, 'w', encoding="utf-8") as srt:
                write_srt(result["segments"], file=srt,
                          line_length=break_lines)
            print("Saved SRT to", os.path.abspath(srt_path))
        elif subtitles_format == "txt":
            txt_path = os.path.join(output_dir, f"{slugify(title)}.txt")
            with open(txt_path, 'w', encoding="utf-8") as txt:
                write_txt(result["segments"], file=txt,
                          line_length=break_lines)
            print("Saved TXT to", os.path.abspath(txt_path))
        else:
            print(f"subtitle type {subtitles_format} is wrong")
            exit(-1)


def get_audio(urls):
    temp_dir = tempfile.gettempdir()

    ydl = yt_dlp.YoutubeDL({
        'quiet': True,
        'verbose': False,
        'format': 'bestaudio',
        "outtmpl": os.path.join(temp_dir, "%(id)s.%(ext)s"),
        'postprocessors': [{'preferredcodec': 'mp3', 'preferredquality': '192', 'key': 'FFmpegExtractAudio', }],
    })

    paths = {}
    for url in urls:
        if url.startswith('https://') or url.startswith("http://"):
            start = time.time()
            result = ydl.extract_info(url, download=True)
            print(
                f"Downloaded audio only \"{result['title']}\" \
                    in {time.time() - start}. Generating subtitles..."
            )
            paths[result["title"]] = os.path.join(
                temp_dir, f"{result['id']}.mp3")
            print(f"audio saved to {paths[result['title']]}")

        elif os.path.exists(url):
            print(f"local file {url}")
            output_mp3 = convert_video_to_audio_ffmpeg(url)
            paths[os.path.splitext(os.path.basename(url))[0]] = output_mp3
            assert os.path.exists(output_mp3)
            print(f"audio saved to {output_mp3}")
        else:
            print(f"url not exist {url}")
    return paths


if __name__ == '__main__':
    main()
