import os
import re
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# 配置路径
DATA_SOURCE_DIR = 'data_source'
FINANCIAL_ANALYSIS_FILE = 'financial_analysis.py'
CONFIG_FILE = 'config.json'

def update_api_key_in_file(api_key):
    """更新financial_analysis.py文件中的API密钥"""
    try:
        with open(FINANCIAL_ANALYSIS_FILE, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 使用正则表达式替换API密钥
        updated_content = re.sub(
            r'DEEPSEEK_API_KEY\s*=\s*["\'][^"\']*["\']',
            f'DEEPSEEK_API_KEY = "{api_key}"',
            content
        )
        
        with open(FINANCIAL_ANALYSIS_FILE, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        return True
    except Exception as e:
        print(f"Error updating API key: {e}")
        return False

def save_config(api_key):
    """保存配置到config.json文件"""
    try:
        config = {'api_key': api_key}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False

def load_config():
    """从config.json文件加载配置"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('api_key', '')
    except Exception as e:
        print(f"Error loading config: {e}")
    return ''

@app.route('/')
def index():
    # 简化模板渲染逻辑，不传递变量
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        if 'files[]' not in request.files:
            flash('没有选择文件', 'error')
            return redirect(request.url)
        
        files = request.files.getlist('files[]')
        
        if not files or all(f.filename == '' for f in files):
            flash('没有选择文件', 'error')
            return redirect(request.url)
        
        saved_files = []
        for file in files:
            if file and file.filename:
                # 确保文件名安全
                filename = file.filename
                file_path = os.path.join(DATA_SOURCE_DIR, filename)
                file.save(file_path)
                saved_files.append(filename)
        
        flash(f'成功上传 {len(saved_files)} 个文件: {", ".join(saved_files)}', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'上传失败: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/update_api_key', methods=['POST'])
def update_api_key():
    try:
        api_key = request.form.get('api_key', '').strip()
        
        if not api_key:
            flash('API密钥不能为空', 'error')
            return redirect(url_for('index'))
        
        # 更新financial_analysis.py文件中的API密钥
        if update_api_key_in_file(api_key):
            # 保存到配置文件
            save_config(api_key)
            flash('API密钥更新成功', 'success')
        else:
            flash('API密钥更新失败', 'error')
            
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'更新失败: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    # 确保data_source目录存在
    if not os.path.exists(DATA_SOURCE_DIR):
        os.makedirs(DATA_SOURCE_DIR)
    
    app.run(debug=True, host='127.0.0.1', port=5000)