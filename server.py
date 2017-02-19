from flask import Flask
app = Flask(__name__)

# Question 1:
# The method below should be called by a web browser to get
# the current web page.
# Are you sure the following method should be a POST method?
# The choices we have are GET, POST, PUT and DELETE
@app.route('/', methods=['POST'])
def hello():
    # Question 2:
    # To print something out when you get a request for '/' route,
    # uncomment the next line:

    #print('Someone just called the "GET /" route')

    # Question 3:
    # To return a simple message, uncomment the next line.
    # Perhaps change the message to something more interesting
    
    #return 'my simple message'
    
    # ... and delete this line
    pass
    

if __name__ == "__main__":
    app.run()
