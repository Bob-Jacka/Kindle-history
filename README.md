# BookManager

## What is it?:

Non - useful app if you have cracked (with "Koreader") Kindle or other e-book and want to save your books.

## Utility modules:

This utility contains several modules to use:

### Book database (Book_db):

Inner nosql database for interaction in interactive or non-interactive mode.
Module used for books actions in database style.

#### module methods:

1. module provide CRUD operations (create, read, update, delete operations)
2. inner syntax interpreter for interactive mode

#### module modes:

1. Interactive - manual BQL command input
2. Non-interactive - auto mode, you need to select commands

### Kindle history (Kindle_history):

Module used for interaction with read file

#### module methods:

1. module provide convenient way to save books that you want.
2. module provide delete books that you want
3. module write history about your already read books

#### module modes:

1. Auto mode - automatically save books in file.
2. Manual mode - ask user about anything.

### Transfer book (Transfer_book):

module for transferring books from your local personal computer to e-book by tcp or ftp internet protocols

#### module modes:

1. TCP mode
2. FTP mode