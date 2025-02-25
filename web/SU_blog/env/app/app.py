from flask import *
import time,os,json,hashlib
from pydash import set_
from waf import pwaf,cwaf

app = Flask(__name__)
app.config['SECRET_KEY'] = hashlib.md5(str(int(time.time())).encode()).hexdigest()

users = {"testuser": "password"}
BASE_DIR = '/var/www/html/myblog/app'

articles = {
    1: "articles/article1.txt",
    2: "articles/article2.txt",
    3: "articles/article3.txt"
}

friend_links = [
    {"name": "bkf1sh", "url": "https://ctf.org.cn/"},
    {"name": "fushuling", "url": "https://fushuling.com/"},
    {"name": "yulate", "url": "https://www.yulate.com/"},
    {"name": "zimablue", "url": "https://www.zimablue.life/"},
    {"name": "baozongwi", "url": "https://baozongwi.xyz/"},
]

class User():
    def __init__(self):
        pass

user_data = User()
@app.route('/')
def index():
    if 'username' in session:
        return render_template('blog.html', articles=articles, friend_links=friend_links)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Invalid credentials", 403
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if users[session['username']] != old_password:
            flash("Old password is incorrect", "error")
        elif new_password != confirm_password:
            flash("New passwords do not match", "error")
        else:
            users[session['username']] = new_password
            flash("Password changed successfully", "success")
            return redirect(url_for('index'))

    return render_template('change_password.html')


@app.route('/friendlinks')
def friendlinks():
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('login'))
    return render_template('friendlinks.html', links=friend_links)


@app.route('/add_friendlink', methods=['POST'])
def add_friendlink():
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('login'))

    name = request.form.get('name')
    url = request.form.get('url')

    if name and url:
        friend_links.append({"name": name, "url": url})

    return redirect(url_for('friendlinks'))


@app.route('/delete_friendlink/<int:index>')
def delete_friendlink(index):
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('login'))

    if 0 <= index < len(friend_links):
        del friend_links[index]

    return redirect(url_for('friendlinks'))

@app.route('/article')
def article():
    if 'username' not in session:
        return redirect(url_for('login'))

    file_name = request.args.get('file', '')
    if not file_name:
        return render_template('article.html', file_name='', content="未提供文件名。")

    blacklist = ["waf.py"]
    if any(blacklisted_file in file_name for blacklisted_file in blacklist):
        return render_template('article.html', file_name=file_name, content="大黑阔不许看")
    
    if not file_name.startswith('articles/'):
        return render_template('article.html', file_name=file_name, content="无效的文件路径。")
    
    if file_name not in articles.values():
        if session.get('username') != 'admin':
            return render_template('article.html', file_name=file_name, content="无权访问该文件。")
    
    file_path = os.path.join(BASE_DIR, file_name)
    file_path = file_path.replace('../', '')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        content = "文件未找到。"
    except Exception as e:
        app.logger.error(f"Error reading file {file_path}: {e}")
        content = "读取文件时发生错误。"

    return render_template('article.html', file_name=file_name, content=content)


@app.route('/Admin', methods=['GET', 'POST'])
def admin():
    if request.args.get('pass')!="SUers":
        return "nonono"
    if request.method == 'POST':
        try:
            body = request.json

            if not body:
                flash("No JSON data received", "error")
                return jsonify({"message": "No JSON data received"}), 400

            key = body.get('key')
            value = body.get('value')

            if key is None or value is None:
                flash("Missing required keys: 'key' or 'value'", "error")
                return jsonify({"message": "Missing required keys: 'key' or 'value'"}), 400

            if not pwaf(key):
                flash("Invalid key format", "error")
                return jsonify({"message": "Invalid key format"}), 400

            if not cwaf(value):
                flash("Invalid value format", "error")
                return jsonify({"message": "Invalid value format"}), 400

            set_(user_data, key, value)

            flash("User data updated successfully", "success")
            return jsonify({"message": "User data updated successfully"}), 200

        except json.JSONDecodeError:
            flash("Invalid JSON data", "error")
            return jsonify({"message": "Invalid JSON data"}), 400
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500

    return render_template('admin.html', user_data=user_data)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=10006)
