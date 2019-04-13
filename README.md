[![Codacy Badge](https://api.codacy.com/project/badge/Grade/55aaf8de4794485dbe10859818f8d9fc)](https://www.codacy.com/app/0x20/newline)

# How this repository works

Everytime a commit is pushed to [this repository](https://github.com/0x20/newline), a webhook `https://hackerspace.gent/newline/pull.php` is called, triggering a `git pull` in the `0x20.be/newline` repository.

- `.htaccess`: This file redirects `/newline` to `/newline/2019`. **This needs to be changed every year.**
- `2015/`, `2016/`, `/20..`: Each year has its own directory. **Add a new directory each year**
- `pull.php`: This file calls `git pull` when accessed. This is needed for automatic sync with github, so **do not change it!**

# Handy information:

If you want to commit from the server itself, use this command to specify your name and email address

```bash
git -c user.name='<NAME>' -c user.email='<EMAIL>' commit -m '<TEXT>'
```

Thanks to: http://writing.markchristian.org/2011/03/10/how-to-deploy-your-code-from-github-automatically.html
