# How this repository works

Everytime a commit is pushed to [this repository](https://github.com/0x20/newline), github posts to `https://0x20.be/newline/pull.php` triggering a `git pull` in the `0x20.be/newline` repository.

- `.htaccess`: This file redirects `/newline` to `/newline/2016`. **This needs to be changed every year.**
- `2015/`, `2016/`, `/20..`: Each year has its own directory. **Add a new directory each year**
- `pull.php`: This file calls `git pull` when accessed. This is needed for automatic sync with github, so **do not change it!**

# Handy information:

If you want to commit from the server itself, use this command to specify your name and email address

  git -c user.name='<NAME>' -c user.email='<EMAIL>' commit -m '<TEXT>'


Thanks to: http://writing.markchristian.org/2011/03/10/how-to-deploy-your-code-from-github-automatically.html
