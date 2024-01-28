# SetMix
Version 0.1

## Description
Terminal based tool to view the average setlist for a tour, utilizing the setlist.fm API

Key Aspects
- Terminal based user interface
- Setlist API for data collection


## Installation
Clone this repository to your local machine:
```bash
git clone https://github.com/adeilertson/setmix
```

Change into the project directory:

```bash
cd SetMix
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
py main.py
```


## Usage

### Searching
You can search by artist and optionally tour name to get tour data. Searching by only artist can
return a large number of results which will take more time to return. The process will prompt you
to confirm the expected amount of data collection.

After collecting the data, the tool will build the average setlist for the tour and display the
songs performed in their average position performed, along with the song name, and the frequency
the song is performed on the tour.

## Updates

## Future Features
- Get setlist for specifc show by adding venue and date search parameters
- Spotify playlist creation