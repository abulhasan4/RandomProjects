from flask import Flask, request, render_template, send_file, jsonify
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})

@app.route('/view', methods=['GET'])
def view_file():
    filename = request.args.get('filename')
    if not filename:
        return 'No filename provided', 400
    
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return 'File not found', 404
    
    df = pd.read_excel(file_path)
    return df.to_json(orient='records')

@app.route('/filter', methods=['POST'])
def filter_data():
    data = request.json
    filename = data.get('filename')
    filters = data.get('filters', [])
    match_type = data.get('match_type', 'exact')
    
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return 'File not found', 404
    
    df = pd.read_excel(file_path)
    
    for col, value in filters.items():
        if match_type == 'contains':
            df = df[df[col].astype(str).str.contains(value, na=False, case=False)]
        else: # Exact match
            df = df[df[col] == value]
    
    filtered_file = os.path.join(UPLOAD_FOLDER, 'filtered.csv')
    df.to_csv(filtered_file, index=False)
    
    return jsonify({'message': 'Data filtered', 'download_url': '/download?filename=filtered.csv'})

@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('filename')
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return 'File not found', 404
    
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
