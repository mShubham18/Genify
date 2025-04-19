from flask import Flask, render_template, request
from components.generate_response import generate_fact
from pipelines.upload_video_pipeline import upload_video_pipeline

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("new_index.html")

@app.route("/upload", methods=["POST"])
def upload():
    title = request.form.get("title")
    domain = request.form.get("domain")
    
    if title and domain:
        # Generate fact based on the title and domain
        fact = generate_fact(title, domain)
        
        # Process the video generation
        resp = upload_video_pipeline(fact)
        
        # Optionally, you can display the response or redirect to another page
        return render_template("new_index.html", response=resp)
    else:
        # Handle the case where no title or domain is provided
        return render_template("new_index.html", error="Please provide both title and domain.")

if __name__ == "__main__":
    app.run(debug=True)
