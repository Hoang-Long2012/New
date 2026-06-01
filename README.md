# New

A simple command-line utility for creating folders and files.

## Features

- Create one or more folders
- Create one or more files
- Automatically create parent directories
- Optional overwrite support
- Confirmation prompt before overwriting
- Text and binary file creation
- Verbose and quiet output modes

## Installation

### From GitHub release

If you are using Windows you can download New_Windows_x64.zip in the releases section below by  
[clicking here](https://github.com/Hoang-Long2012/new/releases/latest) then unzip and enjoy.

### From source

```
git clone https://github.com/yourusername/new.git
cd new/src
python new.py
```

### Build executable

```
pyinstaller --onefile new.py
```

## Usage

### Create folders

```
new Project Docs Assets
```

Result:

```
Project/
Docs/
Assets/
```

### Create files

```
new -f README.md LICENSE src/main.py
```

Result:

```
README.md
LICENSE
src/
└── main.py
```

### Create folders and files together

```
new src tests docs -f README.md LICENSE src/main.py tests/test_main.py
```

Result:

```
src/
tests/
docs/
README.md
LICENSE
src/main.py
tests/test_main.py
```

### Create binary files

```
new -f image.bin data.bin -b
```

### Create files with a specific encoding

```
new -f notes.txt -e utf-8
```

### Overwrite existing files or folders

```
new Project -f README.md -o
```

### Overwrite without confirmation

```
new Project -f README.md -o -y
```

### Verbose mode

```
new Project -v
```

### Quiet mode

```
new Project -q
```

## Options

| Option              | Description                             |
| ------------------- | --------------------------------------- |
| `-f`, `--file`      | Files to create                         |
| `-b`, `--byte`      | Create files in binary mode             |
| `-e`, `--encoding`  | Encoding for text files                 |
| `-o`, `--overwrite` | Overwrite existing files or directories |
| `-y`, `--yes`       | Skip overwrite confirmation             |
| `-v`, `--verbose`   | Show detailed logs                      |
| `-q`, `--quiet`     | Suppress non-critical output            |
| `-V`, `--version`   | Show program version                    |
| `-h`, `--help`   | Show help message                    |

## Examples

Create a Python project skeleton:

```
new src tests docs -f README.md LICENSE src/main.py tests/test_main.py
```

Create a web project skeleton:

```
new css js images -f index.html css/style.css js/app.js
```

Create nested directories automatically:

```
new -f project/src/main.py
```

The `project` and `project/src` directories will be created automatically if they do not already exist.

## License

MIT License

© Copyright (c) 2026 Hoang-Long2012