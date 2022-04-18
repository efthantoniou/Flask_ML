from flask import Flask, url_for, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import network_for_captcha as network




UPLOAD_FOLDER = os.getcwd() + '\\data\\'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}

app = Flask(__name__, template_folder='template')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
now = datetime.now()


@app.route("/", methods=['GET', 'POST'])
def index_upload():
    return render_template('form.html')
    
def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/results", methods=['POST'])
def results():
    if request.method == 'POST':    
        if 'file' not in request.files:
            flash('No files!')
            return redirect(url_for("index_upload"))
        x = 10
        f = request.files['file']
        if f.filename == '':
            flash('No selected file!')
            return redirect(url_for("index_upload"))
        if f and allowed_filename(f.filename):
            file = secure_filename(f.filename)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file)
            f.save(filename)
            
            result = network.run_detector(filename)
            
            return render_template('results.html', value=result)


if __name__ == '__main__':
    app.run(debug=True)



