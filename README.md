# Pumpkin Production in Canada

Pumpkin production project for "Mean, Median, and Moose." If all you want is the charts, they're in the `charts` directory.

## Raw Data
CSV files in the `data` directory contain pumpkin production data extracted from Statistics Canada data.

## Building the Dockerfile
To build the Dockerfile, navigate to the project root directory and run:
```sh
docker build -t pumpkin-production .
```

## Executing the Script
To get a shell inside the Docker container, run:
```sh
docker run --it --rm --name pumpkin pumpkin-production
```

Inside the container shell, run:
```sh
python process_pumpkins.py
```

to generate data from the CSV files. I've already done this - the repository includes a SQLite database named `pumpkin.db`

## Querying the Database

You can query  `pumpkin.db` in place inside the container, or copy the database file to use in your own pumpkin-related project.

## Copying Data from the Container
To copy the data from the container to your local machine, use the following command:
```sh
docker cp pumpkin:/app/charts /local/path
```
