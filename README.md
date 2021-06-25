<h1>Docker installation</h1>
Make sure you have docker installed in your system. Check by using the command:

```bash
docker -v
```
You should see the docker version if you have docker installed on your system. 

You can install Docker from <a href="https://docs.docker.com/desktop/">here</a>

<h1>Configuration</h1>
Inside config/config.json, make sure you have entered configuration properly.

<h1>Running the code</h1>

<h2>Create necessary schema</h2>
The dump for schema is located in the directory sql. Create a new schema OCR_DB in your database and run the queries
in sql/OCR_DB.sql



<h2>Building the image</h2>
Make sure you are inside the directory where the Dockerfile is located. Run the following command:

```bash
docker build -t tesseract .
```

<h2>Run the container</h2>

To run identification job, enter the command:

```bash
docker run \
          --mount type=bind,source=`directory_where_images_are_present`,target=/app/test_image  \
          --rm tesseract load /app/test_image
```

To run verification job, enter the command:

```bash
docker run tesseract verify
```

<h2>Mount logs</h2>
To store logs in logs directory, we need to mount the log path.
For example

```bash
docker run tesseract --mount type=bind,src=`working directory`/logs,dst=/app/logs --rm tesseract verify
```