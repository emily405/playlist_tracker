from git import Repo
import time
import os

repo = Repo('.')
assert not repo.bare

all_commits = list(repo.iter_commits("main", paths='test_playlist.json'))
t = time.strftime("%a, %d %b %Y %H:%M", time.gmtime(all_commits[0].committed_date))

filetext = f'''<!doctype html>
<html>

<head>
    <title>placeholder page</title>
</head>

<body>
last commit was on {t}
</body>

</html>
'''

os.makedirs('webpage', exist_ok=True)
with open("webpage/test_webpage.html", "w") as html_file:
    html_file.write(filetext)