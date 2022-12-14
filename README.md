<p align="center">
  <img src="https://user-images.githubusercontent.com/80219582/192728064-ea98c836-3dbd-42ee-a7af-10f409bf29f6.png" />
</p>

## Summary

The contents of this repository are used to setup an automated pipeline & dashboard using AWS by;

- Ingesting data from several sources in an S3 bucket & storing in a staging schema on AuroraDB
- Pulling data from AuroraDB, cleaning and posting to a production schema
- Dockerizing both Ingestion & Production scripts, pushing to an ECR
- Utilizing Lambda functions to run ECR images for both as prompted by a CloudWatch trigger
- Creating a Dashboard using dash (flask-wrapper framework), dockerizing and hosting on EC2

<p align="center">
  <img src="https://user-images.githubusercontent.com/80219582/193147173-54a33527-8f10-40a6-89c3-2d860e89f013.png" />
</p>

## Dashboard Link

http://44.202.51.236:8080/

## Dockerization terminal commands

Once the dockerfile has been created, the following commands can be used to build & run the container;

**(1) Locally**

```sh
docker build . -t [IMAGE_TAG]
```

```sh
docker run -d new-ingestion
```

**(2) Remotely on AWS**

Retrieve an authentication token and authenticate your Docker client to your registry.
Use the AWS CLI:

```sh
aws ecr get-login-password --region {REGION} | docker login --username AWS --password-stdin {ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com
```

Build the dockerfile - if using an M1 chip, use the following modified command, otherwise build the docker as shown above

```sh
docker build . -t [IMAGE_TAG] --platform "linux/amd64"
```

After the build is completed, tag your image so you can push the image to this repository:

```sh
docker tag [IMAGE_TAG] [ECR_REPOSITORY_LINK]
```

Run the following command to push this image to your newly created AWS repository:

```sh
docker push [ECR_REPOSITORY_LINK]
```

## Running dashboard ECR on EC2 instance

Once an SSH connection is made via the AWS CLI, use the following instructions to run an ECR image on an EC2 instance

Authenticate Docker and ECR

```sh
aws ecr get-login-password --region {REGION} | sudo docker login --username AWS --password-stdin {ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com
```

Pull the image to the EC2 instance

```sh
sudo docker pull {ACCOUNT_ID}.dkr.ecr.{REGION}.amazonaws.com/{ECR_REGISTRY_NAME}:latest
```

Run the container on a port which EC2 listens to (set during EC2 configuration) and pass your .env file

```sh
sudo docker run -d -p 8080:8080 --env-file ./.env {account_id}.dkr.ecr.{region}.amazonaws.com/{ecr_registry_name}
```

### Dependencies

- dash -> https://dash.plotly.com/installationhttps://dash.plotly.com/installation
- dash_bootstrap_components -> https://dash-bootstrap-components.opensource.faculty.ai/docs/quickstart/
- datetime -> https://docs.python.org/3/library/datetime.html
- pandas -> https://pandas.pydata.org/docs/getting_started/index.html
- plotly & plotly.express -> https://plotly.com/python/
- python-dotenv -> https://pypi.org/project/python-dotenv/
- psycopg2-binary -> https://pypi.org/project/psycopg2-binary/
- SQLalchemy (DEPENDENT ON PSYCOPG2) -> https://docs.sqlalchemy.org/en/14/
- s3fs -> https://s3fs.readthedocs.io/en/latest/
