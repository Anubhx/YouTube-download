from flask import Flask, request, send_file, jsonify, render_template
import yt_dlp
import os
import re
import logging

# Initialize the Flask application
app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

def sanitize_filename(filename):
    # Replace any characters that are not allowed in filenames
    return re.sub(r'[<>:"/\\|?*]', '', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    format = data.get('format')
    
    app.logger.info(f"Received request to download video: {url} in format: {format}")

    output_file = None  # Initialize output_file
    
    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        ydl_opts = {
            'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo+bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'noplaylist': True,
            'ffmpeg_location': 'C:/ffmpeg/ffmpeg-7.0.1-essentials_build/bin',  # Ensure this path is correct
        }

        app.logger.info(f"Using ffmpeg at: {ydl_opts['ffmpeg_location']}")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = sanitize_filename(info_dict.get('title', 'untitled'))
            video_ext = 'mp3' if format == 'mp3' else info_dict.get('ext', 'webm')
            output_file = os.path.join('downloads', f"{video_title}.{video_ext}")

        app.logger.info(f"Downloaded file to: {output_file}")

        if os.path.exists(output_file):
            return send_file(output_file, as_attachment=True)
        else:
            raise FileNotFoundError(f"File not found: {output_file}")

    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up the downloaded file after sending it
        if output_file and os.path.exists(output_file):
            os.remove(output_file)
            app.logger.info(f"Removed file: {output_file}")

if __name__ == '__main__':
    app.run(debug=True)
