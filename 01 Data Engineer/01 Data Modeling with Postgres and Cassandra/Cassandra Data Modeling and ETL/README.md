# Data Modeling with Cassandra

## Introduction

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analysis team is particularly interested in understanding what songs users are listening to. Currently, there is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app.

They'd like a data engineer to create an Apache Cassandra database which can create queries on song play data to answer the questions, and wish to bring me on the project. My role is to create a database for this analysis. I'll be able to test the database by running queries given to me by the analytics team from Sparkify to create the results.

## Project Datasets

The directory of CSV files, `event_data`, is partitioned by date. Here are examples of filepaths to two files in the dataset:

```
event_data/2018-11-08-events.csv
event_data/2018-11-09-events.csv
```

## Schema for Song Play Analysis

1. Give me the artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession = 4

```
Table Name: artist_library
column 1: sessionId
column 2: itemInSession
column 3: artist
column 4: song
column 5: length
PRIMARY KEY (sessionId, itemInSession)
```

2. Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182

```
Table Name: artist_user_library
column 1: userId
column 2: sessionId
column 3: itemInSession
column 4: artist
column 5: song
column 6: firstName
column 7: lastName
PRIMARY KEY (userId, sessionId, itemInSession)
```

3. Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'

```
Table Name: user_library
column 1: userId
column 2: firstName
column 3: lastName
column 4: song
PRIMARY KEY (song, userId)
```

## ETL Pipeline

1. Iterate through each event file in `event_data` to process and create a new CSV file in Python
2. Use Apache Cassandra `CREATE` to do data modeling and `INSERT` statements to load processed records into relevant tables
3. Test by running SELECT statements after running the queries on the populated tables

## Getting Started

Execute command `jupyter notebook Project_1B_Project`