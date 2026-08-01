# New

A simple command-line utility for creating folders and files.

---

## Introduction

Windows CMD does not provide a simple built-in command equivalent to touch. New is a small cross-platform utility that creates files and directories with support for templates, timestamps, and inline content.

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
.
├── README.md
├── LICENSE
├── docs/
├── src/
│   └── main.py
└── tests/
    └── test_main.py
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

From pipeline
```
echo Hello | new -f hello.txt -w
```

### Use template files
```
new -f main.py -T template1.txt template2.txt
```

### Timestamp control

Copy access time and modified time from a reference FILE
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

### Create an empty Python file
```
new -f main.py
```

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

Result:

```
project/
└── src/
    └── main.py
```

### Create a file with content
```
new -f hello.txt -w "Hello world"
```

### Create a file from stdin
```
new -f hello.txt -w
```

### Copy content from templates
```
new -f main.py -T header.txt body.txt
```

---

## Note

- Missing parent directories are created automatically.
- Any encoding supported by Python may be used.  
Examples:  
- utf-8
- utf-8-sig
- utf-16
- cp1252
- cp1258
- latin-1
- Default encoding is utf-8.
- When writing inline, you can use unicode escapes like \n, \t, etc to write some special characters like line breaks, tabs, etc. If the escape is not valid, New will write the original string to the file.
- You can read some popular escapes from  
[Escape Sequences](#escape-sequences)
- When the program is waiting for input from stdin you can press Ctrl+Z then Enter on Windows or Control+D on Linux/MacOS to finish, Ctrl+C to cancel.
- The content of all template files is copied directly into the created file.
- Template files are processed in the order specified.
- When a template file is `-`, it is interpreted as stdin.
- To pass a literal file named `-`, use `./-` (Linux/macOS) or `.\-` (Windows).
- You can use wildcard patterns when specifying template files.
- The source code is cross-platform and should work on Windows, Linux and macOS.
- Currently only Windows binaries are officially provided.

---

## Escape Sequences

When using `-w`, `--write` New attempts to decode common escape sequences.  
• Escape sequences are decoded using Python's unicode_escape codec.

| Escape | Meaning |
|---------|---------|
| \n | New line |
| \r | Carriage return |
| \t | Horizontal tab |
| \v | Vertical tab |
| \b | Backspace |
| \f | Form feed |
| \a | Bell |
| \\\ | Backslash |
| \\' | Single quote |
| \\" | Double quote |
| \xNN | Hexadecimal byte |
| \uNNNN | Unicode character |
| \UNNNNNNNN | Unicode character |
| \N{UNICODE NAME} | Unicode character |
| \\{OCTAL} | Unicode character |

### Examples:

```
new -f hello.txt -w "Hello\nWorld"
```

Produces:

```
Hello
World
```

```
new -f tab.txt -w "Name\tValue"
```

Produces:

```
Name    Value
```

```
new -f emoji.txt -w "\u2764"
```

Produces:

```
❤
```

```
new -f symbol.txt -w "\N{BLACK HEART SUIT}"
```

---

## Changelog

See changelog from:
[CHANGELOG.md](CHANGELOG.md)

---

## License

This project is licensed under the [MIT License](LICENSE).  

---

## Contribution

If you'd like to contribute, feel free to submit a pull request.  
If you'd like to report a bug or request a feature, please open an issue.

---

Copyright (c) 2026 Hoang-Long2012
