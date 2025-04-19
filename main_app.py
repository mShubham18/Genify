from flask import Flask, request, render_template
from components.generate_response import generate_fact
from pipelines.upload_video_pipeline import upload_video_pipeline
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload")
def upload():
    if request.method=="POST":
        title = request.form.get("title")
        domain = request.form.get("domain")
        if title or domain:
            fact = generate_fact(title,domain)
            response = upload_video_pipeline(fact,domain)
if __name__=="__main__":
    app.run(debug=True)