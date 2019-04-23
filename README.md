# Git php lint

Git php lint is a Python library which lints the PHP code added to git versioning system.
Lets assume you add a few lines of code or add a new file to your project. 
Before doing any versioning (adding, committing, etc.), you can run the `git-php-lint` command to check for syntax errors.

## Minimal requirements
Make sure PHP, Python3 and GIT are installed.

## Installation

Clone this repo in your machine, then run the following commands

```bash
python3 setup.py install
```

## Usage

#### Basic usage - linting the added PHP code to existing project files.
This command will lint ONLY your newly added bits of code and not the entire file.
```bash
git-php-lint
```
#### File linting - linting the entire file
This commands will lint the newly added bits of code (see above) plus the newly added files,
untracked by git.
```bash
git-php-lint --file-lint
```
#### Debugging the PHP code
You can see a preview of newly added code and the line numbers. 
Useful for debugging the error message from lint.
```bash
git-php-lint --debug
```
#### Compare added code with a git branch
```bash
git-php-lint --with-branch=origin/master
```
The `origin/master` is the default. You can change it to whatever branch you need.

#### Help
```bash
git-php-lint -h
git-php-lint --help
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
