from flask import Flask, request, jsonify, redirect
import http.client
import os
import urllib.parse

app = Flask(__name__)

# Facebook app credentials (ensure these are set as environment variables for security)
# FB_CLIENT_ID = "1060170592495587"
# FB_CLIENT_SECRET = "3086cf79fac4df9b9de6219434e6bf17"
# FB_REDIRECT_URI = "https://your-render-app-url.com/facebook-callback"

# Start Facebook Login
@app.route("/facebook-login", methods=["GET"])
def facebook_login():
    # Redirect user to Facebook's OAuth dialog
    params = {
        "client_id": FB_CLIENT_ID,
        "redirect_uri": FB_REDIRECT_URI,
        "scope": "public_profile,email",
        "response_type": "code"
    }
    fb_auth_url = f"https://www.facebook.com/v11.0/dialog/oauth?{urllib.parse.urlencode(params)}"
    return redirect(fb_auth_url)

@app.route('/')
def hello_world():
    # print("hello world")
    return 'Hello, World!'

# Facebook Redirect URI to handle the callback
@app.route("/facebook-callback", methods=["GET"])
def facebook_callback():
    # return 'Hello, World!'
    code = request.args.get("code")
    if code:
        # Exchange the code for an access token
        conn = http.client.HTTPSConnection("graph.facebook.com")
        payload = urllib.parse.urlencode({
            "client_id": FB_CLIENT_ID,
            "redirect_uri": FB_REDIRECT_URI,
            "client_secret": FB_CLIENT_SECRET,
            "code": code
        })
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        conn.request("POST", "/v11.0/oauth/access_token", payload, headers)
        
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")
    else:
        return "No code provided", 400

if __name__ == "__main__":
    app.run(debug=True)
