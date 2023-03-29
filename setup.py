from setuptools import setup, find_packages

setup(
    version="1.0",
    name="yt_whisper",
    packages=find_packages(),
    py_modules=["yt_whisper"],
    author="Marvid Labs",
    install_requires=[
        'yt-dlp',
        'openai-whisper'
    ],
    description="Generate subtitles for YouTube videos using Whisper",
    include_package_data=True,
)
