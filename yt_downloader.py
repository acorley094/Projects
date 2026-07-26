#!/usr/bin/env python3
'''
Planned Revisoins for v2...
1) regex "shorts" to "watch" 
2) implement pytube Channels to check for uploads
3) write a script to check for new uploads or a csv of urls and downloads newest videos added to playlists
 '''

AUTHOR = 'acorley094'
PROJECT = 'YouTube Video Downloader'

import argparse
from pytube import YouTube, Playlist
from pytube.exceptions import AgeRestrictedError as are
from concurrent.futures import ThreadPoolExecutor
import subprocess
import os
import re

def main():
    # Configure command line argument parser
    parser = argparse.ArgumentParser(description=f"{PROJECT} written by {AUTHOR}", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('url', default='https://www.youtube.com/watch?v=dQw4w9WgXcQ', help='url of video or playlist')
    parser.add_argument('-d', '--directory', default='./Videos/', help='directory for the video files')
    parser.add_argument('-p', '--playlist', default='Playlist/', help='creates an extra directory to save playlists')
    parser.add_argument('-f', '--format', default='webm',  help='video format')
    parser.add_argument('-r', '--resolution', default='4320p',  help='video resolution')
    parser.add_argument('-q', '--quality' , default='160kbps',  help='audio quality (kbps)')
    parser.add_argument('-w', '--framerate' , default=60, type=int,  help='audio quality (kbps)')
    parser.add_argument('-a', '--audio-only', action= 'store_true', help='only downloads audio')
    parser.add_argument('-v', '--video-only', action= 'store_true', help='only downloads video')
    parser.add_argument('-k', '--keep-separate-files', action= 'store_true', help='keep separate audio and video files')   
    parser.add_argument('-t', '--threads', default=16, type=int, help='number of threads to use.')
    args = parser.parse_args()
    config = vars(args)

    # Configure user values from config
        # url
    url_list = []
    x = re.search(r"playlist", config.get('url'))
    if x:
        is_playlist = True
        url_list = Playlist(config.get('url'))
    else:
        is_playlist = False
        url_list.append(config.get('url'))

        # directory and playlist
    if is_playlist:
        directory = os.path.join(config.get('directory'), config.get('playlist'))
    else:
        directory = config.get('directory')
        
        # format
    if config.get('format'):
        format = config.get('format')
    else:
        format = parser.get_default('format')
    
        # resolution
    if config.get('resolution'):
        resolution = config.get('resolution')
    else:
        format = parser.get_default('resolution')
    
        # quality
    if config.get('quality'):
        quality = config.get('quality')
    else:
        if format == 'webm':
            quality = '160kbps'
        elif format == 'mp4':
            quality = '48kbps'

        # frame-rate
    if config.get('framerate'):
        frame_rate = config.get('framerate')
    else:
        frame_rate = parser.get_default('framerate')

        # audio_only
    if config.get('audio_only'):
        audio_only = True
    else:
        audio_only =False

        # video_only
    if config.get('video_only'):
        video_only = True
    else:
        video_only = False

        # keep_separate_files
    if config.get('keep_separate_files'):
        keep_separate_files = config.get('keep_separate_files')
    else:
        keep_separate_files = parser.get_default('keep_separate_files')

    if config.get('threads'):
        threads = config.get('threads')
    else:
        threads = parser.get_default('threads')

    # main loop
    stream_list = []
    video_list = []
    audio_list= []
    
    #use threading
    for url in url_list:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            try:
                check_age_restricted(url)
            except are as e:
                print('Sorry that vid is age restricted. Skipping...')
                continue

            else:
                if video_only:
                # Pass 'directory' instead of 'config' to the functions
                    executor.submit(video_list.append(get_video_streams(url, format, resolution, frame_rate)))
                elif audio_only:
                    executor.submit(audio_list.append(get_audio_streams(url, quality, format)))
                else:
                    executor.submit(stream_list.append(get_video_streams(url, format, resolution, frame_rate)))
                    executor.submit(stream_list.append(get_audio_streams(url, quality, format)))
                    

        # download video(s)
        file_list = []
        audio_file=''
        video_file=''
        # use threading
        with ThreadPoolExecutor(max_workers=config.get('threads')) as executor:
            if video_only:
                for video in video_list:
                    try:
                        # Pass 'directory' instead of 'config' to the function
                        executor.submit(file_list.append(download_video(video, directory, format)))
                    except Exception as e:
                        print(f'Download error: {e}')
                        continue
                video_file = str(file_list[0])
            
            elif audio_only:
                for audio in audio_list:
                    try:
                        # Pass 'directory' instead of 'config' to the function
                        executor.submit(file_list.append(download_video(audio, directory, format)))
                    except Exception as e:
                        print(f'Download error: {e}')
                        continue
                audio_file = str(file_list[0])
            else:
                for stream in stream_list:
                    try:
                        # Pass 'directory' instead of 'config' to the function
                        executor.submit(file_list.append(download_video(stream, directory, format)))
                    except Exception as e:
                        print(f'Download error: {e}')
                        continue

                    # Get video and audio filenames
                    if len(file_list) >=2:
                        video_file = str(file_list[0])
                        audio_file = str(file_list[1])

   

    # Get video titles
    video_titles = [stream.title for stream in stream_list if stream is not None]

    # Merge audio and video
    if  video_file and audio_file:
        merge_all_files(file_list, directory, keep_separate_files)
        # merge_audio_video(video_file, audio_file, directory, video_titles)


def get_video_streams(url, format, resolution, frame_rate):
    try:
        s = YouTube(url).streams
    except are as e:
        print(f'Skipping age-restricted video {url}...')
        return None
    list = []

    # Check resolution
    r = check_resolution(resolution, s, format)
    resolution = r
    # Check frame rate
    frames = check_frame_rate(resolution, frame_rate, s, format)
    frame_rate = frames

    for item in s:
        if item.mime_type == format and item.resolution == resolution and item.fps == frame_rate:
            list.append(item)

    streams = s.filter(resolution=resolution, mime_type=f'video/{format}', fps=frame_rate)

    # show available streams
    #print_available_streams(streams)
    for item in streams:
        if item:
            print(f'\nVideo info...')
            print(f'Title: {item.title}')
            print(f'Resolution: {item.resolution}')
            print(f'Frame Rate: {item.fps}')
            print(f'File type: {item.mime_type} ')
            print(f'Size: {item.filesize_mb} MB')
            return streams.first()
        else:
            print('Error in video config...')
            print(f'Format: {format}')
            print(f'Resolution: {resolution}')
            quit()


def get_audio_streams(url, quality, format):
    try:
        s = YouTube(url).streams
    except are as e:
        print(f'Skipping age-restricted video {url}...')
        return None
    list = []
    # Check audio quality
    qual = check_audio_quality(format,quality,s)
    quality = qual

    for item in s:
        if item.mime_type == format and item.abr == quality:
            list.append(item)

    streams = s.filter(mime_type=f'audio/{format}', abr=quality)

    # show available streams
    #print_available_streams(streams)

    for item in streams:
        if item:
            print(f'\nAudio info...')
            print(f'Title: {item.title}')
            print(f'File type: {item.mime_type} ')
            print(f'Audio Quality: {item.abr} ')
            print(f'Size: {item.filesize_mb} MB')
            return streams.first()
        else:
            print('Error in video config...')
            print(f'Format: {format}')
            print(f'Audio Quality: {qual}')
            quit()


def check_age_restricted(url):
    if YouTube(url).age_restricted:
        print("Video is Age Restricted.")
        print("Skipping...")
        return True


def download_video(video_stream, path, format):
    t = ''
    if video_stream:
        print(f'\nDownloading...')
        print(f'Title: {video_stream.title}')
        print(f'File type: {video_stream.mime_type}')
        print(f'File size: {video_stream.filesize_mb} MB')

        if video_stream.type == 'video':
            try:
                t = f'_video.{format}'
            except are as e:
                print(f'Video is age restricted: {e}')
                print('Skipping...')
                return None
            print(f'Resolution: {video_stream.resolution}')

        if video_stream.type == 'audio':
            t = f'_audio.{format}'
            print(f'Audio Quality: {video_stream.abr} ')

        # f = "".join([c for c in video_stream.title if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
        # f = "".join([c if c.isalpha() or c.isdigit() or c == ' ' else '_' for c in video_stream.title]).rstrip()
        f = "".join([c for c in video_stream.title if c.isalpha() or c.isdigit() or c == ' ']).rstrip()
        f = f.replace(' ', '_')


        if '_video' in t:
            f = f.replace('_video', '')
        elif '_audio' in t:
            f = f.replace('_audio', '')

        try:
            file = video_stream.download(output_path=path, filename=str(f'{f}{t}'), max_retries=10)
            return file
        except Exception as e:
            print(f'An error occurred: {e}')

    else:
        print('Video stream not available.')
        print('Skipping...')
        return None



def merge_audio_video(vid, aud, directory, titles):
    o_filename = os.path.join(directory, f'{titles[0]}')

    # Ensure that the correct directory is used in the command
    cmd = [
        'ffmpeg',
        '-y',
        '-i', vid,
        '-i', aud,
        '-c:v', 'copy',
        '-c:a', 'copy',
        o_filename
    ]

    # Print the command for debugging purposes
    print('Running command:', ' '.join(cmd))

    try:
    # Run the command
        subprocess.run(cmd)
        print('Merging successful')
    except subprocess.CalledProcessError as e:
        print(f'Merging failed with error: {e}')

    print(f'Merged video and audio saved to: {o_filename}')


def merge_all_files(file_list, directory, keep_separate_files):
    for pair in file_list:
        if pair is None:
            print('Skipping None pair.')
            continue


        video_file = pair
        audio_file = pair.replace('_video', '_audio')
        output_file = pair.replace('_video', '')

        if audio_file and video_file:
            merge_audio_video(video_file, audio_file, directory, [output_file])


        # Delete separated files if keep_separate_files is False
        if not keep_separate_files:
            try:
                os.remove(os.path.join(directory, video_file))
                os.remove(os.path.join(directory, audio_file))
                print(f"Separated files deleted: {video_file}, {audio_file}")
            except OSError as e:
                print(f"Error deleting separated files: {e}")


def print_available_streams(streams):
    print('Available Streams...')
    print('================================')
    for item in streams:
        if item:
            print(f'\nStream Info...')
            print(f'Title: {item.title}')
            if item.type=='video':
                print(f'Resolution: {item.resolution}')
                print(f'Frame Rate: {item.fps}')
            if item.type=='audio':
                print(item.abr)
            print(f'File type: {item.mime_type} ')
            print(f'Size: {item.filesize_mb} MB')
    print('================================')
    

def check_resolution(resolution, s, format):
    list = []
    print('Checking video streams for desired resolution:')
    # check resolution
    while not list:
        for item in s:
            if item.mime_type == f'video/{format}' and item.resolution == resolution:
                list.append(item)

        if not list:
            print(f'{resolution} not available. Checking for next highest resolution...')

            if resolution == '144p':
                break

            elif resolution =='240p':
                resolution = '144p'

            elif resolution == '360p':
                resolution = '240p'

            elif resolution == '480p':
                resolution = '360p'
            
            elif resolution == '720p':
                resolution = '480p'

            elif resolution == '1080p':
                resolution = '720p'

            elif resolution == '1440p':
                resolution = '1080p'

            elif resolution == '2160p':
                resolution = '1440p'

            elif resolution == '4320p':
                resolution = '2160p'

    return resolution


def check_frame_rate(resolution, framerate, s, format):
    list = []
    print('Checking video streams for desired framerate:')
    # check framerate
    while not list:
        for item in s:
            if item.mime_type == f'video/{format}' and item.resolution == resolution and item.fps == framerate:
                list.append(item)

        if not list:
            print(f'{framerate}fps not available. Checking for next highest framerate...')
            next_framerate = None

            if framerate == 12:
                next_framerate = None
            elif framerate == 24:
                next_framerate = 12
            elif framerate == 25:
                next_framerate = 24
            elif framerate == 30:
                next_framerate = 25
            elif framerate == 50:
                next_framerate = 30
            elif framerate == 60:
                next_framerate = 50
            elif framerate == 90:
                next_framerate = 60
            elif framerate == 120:
                next_framerate = 90
            elif framerate == 144:
                next_framerate = 120

            if next_framerate is None:
                break

            framerate = next_framerate

    return int(framerate)



def check_audio_quality(format,quality, s):
    list = []
    f = format
    print('Checking audio streams for desired quality:')
    # check quality
    while not list:
        for item in s:
            if item.mime_type == f'audio/{format}' and item.abr == quality:
                list.append(item)
            
        if not list:
            print(f'{quality} not available. Checking for next highest bitrate...')

        next_quality = None

        if f == 'mp4' or 'mp3':

            if quality == '48kbps':
                return None

            if quality == '128kbps':
                next_quality = '48kbps'

            if quality == '192kbps':
                next_quality = '128kbps'
            
            if quality == '384kbps':
                next_quality = '192kbps'
            quality = next_quality            

        elif f == 'webm':
            if quality == '50kbps':
                return None

            if quality == '70kbps':
                next_quality = '50kbps'

            if quality == '160kbps':
                next_quality = '70kbps'
            quality = next_quality

        if next_quality == None:
            break

    return quality


if __name__ == '__main__':
    main()
