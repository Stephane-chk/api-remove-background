# API for removing background from image

## Requirements

 - Python >= 3.8
 - Upgrade your pip

```sh
pip install --upgrade pip
```
 - Install dependancies of the project

```sh
pip install Flask gunicorn python-dotenv urllib3 rembg
```

  - To run the project: 
```sh
python3.8 main.py
```
  - To run the project with gunicorn: 
```sh
gunicorn --access-logfile app.log main:app -b 0.0.0.0:9090
```

## API Reference

#### Remove background from image

```http
  GET /rm-bg
```

| Parameter | Type            | Description                 |
| :-------- | :-------------- | :-------------------------- |
| `token`   | **Text format** | **Required** token (see .env file)          |
| `files`   | **Files**       | **Required** the image file |

#### Reponse 
an image without the background in PNG format


