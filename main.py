from flask import Flask, render_template, request
from summarizer import read_txt, read_pdf, clean, ai_summarize

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")

        if not file:
            return render_template("index.html", summary="No file uploaded.")

        filename = file.filename.lower()

        if filename.endswith(".txt"):
            text = read_txt(file)
        elif filename.endswith(".pdf"):
            text = read_pdf(file)
        else:
            return render_template("index.html",
                                   summary="Unsupported file format. Please upload TXT or PDF.")

        cleaned = clean(text)

        # Limit check BEFORE summarizing
        MAX_WORDS = 5000
        word_count = len(cleaned.split())

        if word_count > MAX_WORDS:
            return render_template(
                "index.html",
                summary=f"File too large ({word_count} words). Max allowed: {MAX_WORDS} words."
            )

        # Summarize
        summary = ai_summarize(cleaned)
        return render_template("index.html", summary=summary)
    return render_template("index.html", summary=None)

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
