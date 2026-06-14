from flask import Flask, render_template, request, send_from_directory
import os
import logging
from datetime import datetime
from generate_song import generate_song, logger as song_logger

app = Flask(__name__)

# Configure Flask logging to use the same logger as generate_song
logging.getLogger("werkzeug").setLevel(logging.WARNING)

# Get the logger from generate_song module for consistency
logger = song_logger

OUTPUT_FILE = "song.mp3"

logger.info("=" * 60)
logger.info("Flask application initialized")
logger.info("=" * 60)

@app.route("/", methods=["GET"])
def index():
    logger.info("GET / - Index page requested")
    return render_template(
        "index.html",
        generated=False,
        output_file=OUTPUT_FILE,
        lyrics_text="",
        style_choice="إلكتروني",
        tempo="",
    )

@app.route("/generate", methods=["POST"])
def generate():
    logger.info("=" * 70)
    logger.info("POST /generate - Song generation request received from Flask")
    logger.info("=" * 70)
    
    # Log received form data
    lyrics_text = request.form.get("lyrics_text", "").strip()
    style_choice = request.form.get("style_choice", "إلكتروني").strip()
    tempo_raw = request.form.get("tempo", "").strip()
    
    logger.info("Form data received:")
    logger.info("  - Lyrics text: %d characters", len(lyrics_text))
    logger.info("  - Style choice: %s", style_choice)
    logger.info("  - Tempo input: %s", tempo_raw or "(empty)")
    
    try:
        tempo = int(tempo_raw) if tempo_raw else None
    except ValueError:
        logger.warning("Invalid tempo value provided: %s, using None", tempo_raw)
        tempo = None

    if not lyrics_text:
        logger.info("No lyrics provided, using default lyrics")
        lyrics_text = "نَشامى… نَشامى… هايبَه وگُوَّه"

    logger.info("Starting song generation...")
    try:
        generate_song(
            output_file=OUTPUT_FILE,
            lyrics_text=lyrics_text,
            style=style_choice,
            tempo_override=tempo,
        )
        logger.info("Song generation completed, preparing response")
    except Exception as e:
        logger.error("Song generation failed in Flask route: %s", e, exc_info=True)
        return render_template(
            "index.html",
            generated=False,
            error=f"Failed to generate song: {str(e)}",
            lyrics_text=lyrics_text,
            style_choice=style_choice,
            tempo=tempo_raw,
        )

    logger.info("=" * 70)
    logger.info("Rendering success response")
    logger.info("=" * 70)
    
    return render_template(
        "index.html",
        generated=True,
        output_file=OUTPUT_FILE,
        lyrics_text=lyrics_text,
        style_choice=style_choice,
        tempo=tempo_raw,
    )

@app.route("/download")
def download():
    logger.info("GET /download - MP3 download requested")
    directory = os.path.abspath(os.path.dirname(__file__))
    if os.path.exists(OUTPUT_FILE):
        file_size = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
        logger.info("Serving MP3 file: %s (%.2f MB)", OUTPUT_FILE, file_size)
    else:
        logger.warning("MP3 file not found: %s", OUTPUT_FILE)
    return send_from_directory(directory=directory, path=OUTPUT_FILE, as_attachment=True)


if __name__ == "__main__":
    logger.info("Starting Flask development server...")
    app.run(debug=True, host="0.0.0.0", port=5000)
