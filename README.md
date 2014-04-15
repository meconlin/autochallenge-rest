automation-challenge REST api
=====================

This is a simple [flask](http://flask.pocoo.org/docs/) app with a very simple json api  

It keeps count of words PUT
It displays the count of all words or a specific word via GET

### API Endpoints

/words          - list all words and counts
/word/<word>    - GET word count or PUT word

Examples:  
```
curl -XPUT http://localhost:5000/word/chicken -d'{"word":"chicken"}'
{
  "okay": "true"
}

curl -XGET http://localhost:5000/words
{
  "chicken": 12, 
  "taco": 2
}

curl -XGET http://localhost:5000/word/taco
{
  "taco": 2
}

```

### Installation

This was built with Python 2.6.6  

Install pip requirements  
```
$>virtualenv env  
$>. env/bin/activate  
$>pip install -r requirements.txt  
```

Init DB  
```
$>. env/bin/activate  
$>python  
>>>from words import init_db  
>>>init_db()  

```

### Run the flask app

```
$>. env/bin/activate
$>python app.py
```

You can interact with the API on localhost:5000


Reference
[Automation Challenges](https://github.com/meconlin/automation-challenges)
[]()

