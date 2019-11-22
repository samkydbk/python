import flask

# @app.route('/aaa')
# def hello():
#     return '你好啊'

html_txt = """
<!DOCTYPE html>
<html>
    <body>
        <h2>get请求</h2>
        <form method='post'>
        <input type='submit' value='按下我发送post请求' />
        </form>
    </body>
</html>        
"""
app = flask.Flask(__name__)
@app.route('/html', methods=['GET', 'POST'])
def hello():
    if flask.request.method == 'GET':
        return html_txt
    else:
        return '已收到post请求'
if __name__ == '__main__':
    app.run()