from flask import Flask, render_template
app = Flask("main")

# # Method 1
# @app.route('/left_most_scan')
# def left_most_scan():
# 	return render_template('left_most_scan')

# Method 4
@app.route('/user_select')
def user_select():
	return render_template('user_select.html')
