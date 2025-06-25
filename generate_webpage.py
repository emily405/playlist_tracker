from git import Repo
import json
import time
import os

repo = Repo('')
assert not repo.bare

test_commits = list(repo.iter_commits("main", paths='test_playlist.json'))
t_test = time.strftime("%a, %d %b %Y %H:%M", time.gmtime(test_commits[0].committed_date))

all_commits = list(repo.iter_commits("main", paths='yeehaw.json'))
t_yeehaw = time.strftime("%a, %d %b %Y %H:%M", time.gmtime(all_commits[0].committed_date))

html = '''<!doctype html>
<html>

<head>
    <title>test playlist tracker</title>
    <meta name="description" content="Tracking songs added and removed form the yeehaw playlist">
    <meta name="keywords" content="yeehaw playlist spotify">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link href="style.css" rel="stylesheet" type="text/css" media="all">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Dosis">
</head>

<body>

    <h1>test playlist tracker</h1>

    <a id="test_section"></a>
    <h2>Test Section</h2>

'''

html = html + f'last test commit was on {t_test}'
html = html + f'last yeehaw commit was on {t_yeehaw}'

html = html + f'yeehaw commits={all_commits}'


for commit in all_commits[:-1]:
    f0 = json.load(commit.tree['yeehaw.json'].data_stream)
    f0_date = commit.committed_datetime
    commit_prev = commit.parents[0]
    f1 = json.load(commit_prev.tree['yeehaw.json'].data_stream)
    added_songs = [s for s in f0 if s not in f1]
    removed_songs = [s for s in f1 if s not in f0]

    for addition in added_songs:
        newrow = f'''<br>
        <span class="date">{addition["added"]}</span>
        <span class="pm">+</span>
        <span class="song">{addition["name"]}</span>
        <iframe src="https://open.spotify.com/embed/track/{addition["id"]}" ></iframe> '''

        html = html + newrow

    for removal in removed_songs:
        newrow = f'''<br>
        <span class="date">{f0_date}</span>
        <span class="pm">+</span>
        <span class="song">{removal["name"]}</span>
        <iframe src="https://open.spotify.com/embed/track/{removal["id"]}" ></iframe> '''

        html = html + newrow



endstring = '''</body>

</html>
'''

html = html + endstring

os.makedirs('webpage', exist_ok=True)
with open("webpage/index.html", "w") as html_file:
    html_file.write(html)