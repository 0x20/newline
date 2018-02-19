# How this repository works

Everytime a commit is pushed to [this repository](https://github.com/0x20/newline), github posts to `https://hackerspace.gent/newline/pull.php` triggering a `git pull` in the `0x20.be/newline` repository, and a parser script generates a pentabarf XML from the JSON conference schedule.

- `.htaccess`: This file redirects `/newline` to `/newline/2018`. **This needs to be changed every year.**
- `2015/`, `2016/`, `/20..`: Each year has its own directory. **Add a new directory each year**
- `pull.php`: This file calls `git pull` when accessed. This is needed for automatic sync with github, so **do not change it!**

# Schedule parser

A parser script reads the newline schedule json data file (<year>/json/data.json) and generates a Pentabarf XML (<year>/xml/pentabarf.xml).

## Requirements

The python parser script relies on these packages :

* lxml
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
