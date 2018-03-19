[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7b6d966b3f684db185dfaa8112d4f5de)](https://app.codacy.com/app/ruleant/newline?utm_source=github.com&utm_medium=referral&utm_content=0x20/newline&utm_campaign=badger)
[![Build Status](https://travis-ci.org/0x20/newline.svg?branch=master)](https://travis-ci.org/0x20/newline)

# How this repository works

Everytime a commit is pushed to [this repository](https://github.com/0x20/newline), a Travis-CI is triggered. The job validates the Newline JSON schedule and tests the parser script. On a successful Travis build a webhook `https://hackerspace.gent/newline/pull.php` is called, triggering a `git pull` in the `0x20.be/newline` repository, and a parser script generates a pentabarf XML from the JSON conference schedule.

- `.htaccess`: This file redirects `/newline` to `/newline/2018`. **This needs to be changed every year.**
- `2015/`, `2016/`, `/20..`: Each year has its own directory. **Add a new directory each year**
- `pull.php`: This file calls `git pull` when accessed. This is needed for automatic sync with github, so **do not change it!**
- `.travis.yml`: configuration for the Travis CI build job
- `schedule_parser.py` : python script that generates a Pentabarf XML file from the Newline schedule JSON file.
- `test` : folder with data to test the `schedule_parser.py` script.

# Schedule parser

A parser script reads the newline schedule json data file (\<year\>/json/data.json) and generates a Pentabarf XML (\<year\>/xml/pentabarf.xml).

## Requirements

The python parser script relies on these packages :

* lxml
* jsonschedule
* python-pentabarf-xml

Install depedencies by running

```bash
pip install -r requirements.txt
```

# Handy information:

If you want to commit from the server itself, use this command to specify your name and email address

```bash
git -c user.name='<NAME>' -c user.email='<EMAIL>' commit -m '<TEXT>'
```

Thanks to: http://writing.markchristian.org/2011/03/10/how-to-deploy-your-code-from-github-automatically.html
