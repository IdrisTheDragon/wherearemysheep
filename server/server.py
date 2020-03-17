import os
import cv2
import numpy as np
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

from finders import Templating, Thresholding
from sheepfinder import ImageManager

UPLOAD_FOLDER = 'images/uploaded'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/clearuploads')
def clear_uploads():
    os.rmtree(app.config['UPLOAD_FOLDER'])
    os.mkdir(app.config['UPLOAD_FOLDER'])
    return "todo implement"

@app.route('/uploads')
def uploads_list():
    list_of_files = {}
    for filename in os.listdir(UPLOAD_FOLDER):
        list_of_files[filename] = '/uploads/' + filename
    return list_of_files

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('upload.html')

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/templating')
def templating():
    if 'filename' not in request.args:
        return 'please provide filename argument e.g  \\templating?filename=example.png',400

    if 'templateSize' in request.args:
        templateSize = request.args['templateSize']
    else:
        templateSize = 15

    template = np.full((templateSize, templateSize), 0, dtype=np.uint8)

    template = cv2.circle(template, (int(templateSize / 2), int(templateSize / 2)), 5, 255, cv2.FILLED)
    m = Templating(template, 0.50)
    filename = request.args['filename']
    filepath = UPLOAD_FOLDER+'/'+ secure_filename(filename)

    im = ImageManager(filepath)
    im.singleLayerFind(m,0)
    templateFile = filename.rsplit('.', 1)[0] + '_template.' + filename.rsplit('.', 1)[1]
    templateFilepath = filepath.rsplit('.', 1)[0] + '_template.' + filepath.rsplit('.', 1)[1]
    im.saveIntermidiary(templateFilepath)
    im.outline_mammal()
    outlinedFile = filename.rsplit('.', 1)[0] + '_template_outlined.' + filename.rsplit('.', 1)[1]
    outlinedFilepath = filepath.rsplit('.', 1)[0] + '_template_outlined.' + filepath.rsplit('.', 1)[1]
    im.saveOutlined(outlinedFilepath)

    return render_template('result.html', title='results', intermidaryFile=templateFile, outlinedFile=outlinedFile)

@app.route('/thresholding')
def thresholding():
    if 'filename' not in request.args:
        return 'please provide filename argument e.g  \\thresholding?filename=example.png',400

    if 'threshold' in request.args:
        threshold = request.args['threshold']
    else:
        threshold = 220

    m = Thresholding(threshold_value=threshold)

    filename = request.args['filename']
    filepath = UPLOAD_FOLDER + '/' + secure_filename(filename)
    im: ImageManager = ImageManager(filepath)
    im.singleLayerFind(m, 0)
    thresholdFile = filename.rsplit('.', 1)[0] + '_threshold.' + filename.rsplit('.', 1)[1]
    thresholdFilepath = filepath.rsplit('.', 1)[0] + '_threshold.' + filepath.rsplit('.', 1)[1]
    im.saveIntermidiary(thresholdFilepath)
    im.outline_mammal()
    outlinedFile = filename.rsplit('.', 1)[0] + '_threshold_outlined.' + filename.rsplit('.', 1)[1]
    outlinedFilepath = filepath.rsplit('.', 1)[0] + '_threshold_outlined.' + filepath.rsplit('.', 1)[1]
    im.saveOutlined(outlinedFilepath)

    return render_template('result.html', title='results', intermidaryFile=thresholdFile, outlinedFile=outlinedFile)


if __name__ == '__main__':
    app.debug = True
    app.run()