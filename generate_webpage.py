from git import Repo
import json
import time
import os

def artist_string(artist_list):
    artist_string = artist_list[0]
    if len(artist_list)>1:
        for n, artist in enumerate(artist_list[1:]):
            artist_string = artist_string + f', {artist}'
    return artist_string

repo = Repo('.')
assert not repo.bare

all_commits = list(repo.iter_commits("main", paths='yeehaw.json'))
t_yeehaw = time.strftime("%a, %d %b %Y %H:%M", time.gmtime(all_commits[0].committed_date))

html = '''<!doctype html>
<html>

<head>
    <title>yeehaw playlist tracker</title>
    <meta name="description" content="Tracking songs added and removed from `Hangman' Adam Page's yeehaw playlist">
    <meta name="keywords" content="yeehaw playlist spotify">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link href="style.css" rel="stylesheet" type="text/css" media="all">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Dosis">
</head>

<body>

    <h1>yeehaw playlist tracker</h1>

'''

html = html + f'The most recent playlist update was on {t_yeehaw}'

for commit in all_commits[:-1]:
    f0 = json.load(commit.tree['yeehaw.json'].data_stream)
    f0_date = commit.committed_datetime
    commit_prev = commit.parents[0]
    f1 = json.load(commit_prev.tree['yeehaw.json'].data_stream)
    added_songs = [s for s in f0 if s not in f1]
    removed_songs = [s for s in f1 if s not in f0]

    for addition in added_songs:
        # date = addition["added"].strftime('%d %b %Y')
        date = f0_date.strftime('%d %b %Y')
        newrow = f'''<br>
        <span class="date">{date}</span>
        <span class="pm">+</span>
        <span class="song">{addition["name"]}</span>
        <span class="artist">{artist_string(addition['artists'])}</span>
        <iframe src="https://open.spotify.com/embed/track/{addition["id"]}" ></iframe> '''

        html = html + newrow

    for removal in removed_songs:
        date = f0_date.strftime('%d %b %Y')
        newrow = f'''<br>
        <span class="date">{date}</span>
        <span class="pm">-</span>
        <span class="song">{removal["name"]}</span>
        <span class="artist">{artist_string(removal['artists'])}</span>
        <iframe src="https://open.spotify.com/embed/track/{removal["id"]}" ></iframe> '''

        html = html + newrow



endstring = '''</body>

</html>
'''

html = html + endstring

os.makedirs('webpage', exist_ok=True)
with open("webpage/index.html", "w") as html_file:
    html_file.write(html)