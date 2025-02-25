from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)

import sys

import subprocess

import os

"""
HINT: RCE me! 
"""

INDEX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Python Executor</title>
</head>
<body>
   <h1>Welcome to PyExector</h1>

   <textarea id="code" style="width: 100%; height: 200px;" rows="10000" cols="10000" ></textarea>

   <button onclick="run()">Run</button>

    <h2>Output</h2>
    <pre id="output"></pre>

    <script>
        function run() {
            var code = document.getElementById("code").value;

            fetch("/run", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    code: code
                })
            })
            .then(response => response.text())
            .then(data => {
                document.getElementById("output").innerText = data;
            });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def hello():
    return INDEX_HTML

@app.route("/run", methods=["POST"])
def runCode():
    code = request.json["code"]
    cmd = [sys.executable,  "-i", f"{os.getcwd()}/audit.py"]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    return p.communicate(input=code.encode('utf-8'))[0]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)