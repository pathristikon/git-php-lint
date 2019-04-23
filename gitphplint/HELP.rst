Usage: git-php-lint [options]

Options:
    --debug                             outputs the added php for debug purposes

    --with-branch=[origin/master]       compare the files with specified origin or
                                        branch. Default: origin/master

    --file-lint                         Instead of linting the bit of code provided
                                        by git, lint the file itself

                                        [Note] If this parameter is provided, it will lint
                                        also the newly added files (git untracked files)

     -h || --help                       get help