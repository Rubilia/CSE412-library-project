# CSE 412 Library project

## Installation instructions

```
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

Open browser and navigate to http://0.0.0.0:8000