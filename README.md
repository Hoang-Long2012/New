# New

A simple command-line utility for creating folders and files.

---

## Features

- Create one or more folders
- Create one or more files
- Automatically create parent directories
- Optional overwrite support
- Confirmation prompt before overwriting
- Text and binary file creation
- Copy file timestamps from reference files
- Custom access/modified time support
- Read from template files or stdin
- Write inline content to files
- Verbose and quiet output modes

---

## Installation

### From GitHub release
Download the release archive, extract, and run from:
[Latest release page](https://github.com/Hoang-Long2012/new/releases/latest)

### From source
```
git clone https://github.com/Hoang-Long2012/new.git
cd new/src
python new.py
```

### Build executable
```
pip install pyinstaller
pyinstaller --onefile --clean --optimize 2 new.py
```

---

## Usage

### Create folders
```
new Project Docs Assets
```

or
```
new -d Project Docs Assets
```

### Create files
```
new -f README.md LICENSE src/main.py
```

### Create folders and files together
```
new src tests docs -f README.md LICENSE src/main.py tests/test_main.py
```

### Create binary files
```
new -f image.bin data.bin -b
```

### Set encoding
```
new -f notes.txt -e utf-8
```

### Overwrite existing files/folders
```
new Project -f README.md -o
```

### Overwrite without confirmation
```
new Project -f README.md -o -y
```

### Write content to file

Inline text
```
new -f hello.txt -w "Hello world"
```

From stdin
```
new -f input.txt -w
```

### Use template files
```
new -f main.py -T template1.txt template2.txt
```

### Timestamp control

Copy timestamp from reference
```
new -f file.txt -r reference.txt
```

Set access and modified time
```
new -f file.txt -a 1234.56 -m 1234.56
```

Disable timestamp update on existing files
```
new -f file.txt -c
```

### Output mode
Verbose mode
```
new Project -v
```

Quiet mode
```
new Project -q
```

---

## Options

- -d, --directory: Create folders
- -f, --file: Create files
- -b, --byte: Binary mode
- -e, --encoding: File encoding
- -o, --overwrite: Overwrite existing
- -y, --yes: Skip confirmation
- -w, --write: Write content to file
- -T, --template: Copy template content
- -r, --reference: Copy timestamps from file
- -a, --access-time: Set access time
- -m, --modified-time: Set modified time
- -t, --time: Set both timestamps
- -c, --no-change-timestamp: Do not update timestamps on existing files
- -v, --verbose: Detailed logs
- -q, --quiet: Minimal output
- -V, --version: Show version
- -h, --help: Show help

---

## Examples

### Python project skeleton
```
new src tests docs -f README.md LICENSE src/main.py tests/test_main.py
```

### Web project skeleton
```
new css js images -f index.html css/style.css js/app.js
```

### Auto-create nested directories
```
new -f project/src/main.py
```

---

## Note

- Missing parent directories are created automatically.
- When writing inline, you can use unicode escapes like \n, \t, etc to write some special characters like line breaks, tabs, etc. If the escape is not valid, New will write the original string to the file.
- When the program is waiting for input from stdin you can Press Ctrl+Z then Enter on Windows or Control+D on Linux, MacOS to finish, Ctrl+C to cancel.
- When transmitting - to -T; --template will make New stop and wait for stdin, if you want to pass a file named exactly - to New please specify using ./- on Linux or MacOS, .\- on Windows.
- Options -w; --write and -t; --template is currently only applicable to text files.
- The source code is cross-platform and should work on Windows, Linux and macOS.
- Currently only Windows binaries are officially provided.

---

## Changelog

See changelog from:
[CHANGELOG.md](https://github.com/Hoang-Long2012/new/blob/main/CHANGELOG.md)

---

## License

MIT License  
Copyright (c) 2026 Hoang-Long2012
