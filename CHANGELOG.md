# Changelog

## New version 1.5

- applied -w; --write and -t; --Template for -b; --bytes, you can now use -w; --write and -t; --template with -b; --bytes.
- Now if the invalid unicode escape character New will display an warning instead of silent as before.
- Now encoding of the files you pass to -t; --Template can be specified with -e; --encoding.

----

## New version 1.4

- Added -w; --write for writing inline or stdin content into files
- Added -T; --template for copying content from template files
- Added -r; --reference for copying timestamps from another file
- Added -t; --time for setting both access and modified time
- Improved timestamp handling and fallback logic
- Improved file writing system and statistics tracking
- Improved CLI validation rules
- Better error handling for filesystem and input operations
- Internal refactor of file and folder creation pipeline
- Improved cli behavior.
- Added new timestamp formats.

----

## New version 1.3

- Added -a; --access-time
- Added -m; --modified-time
- Added -c; --no-change-timestamp
- Improved help output
- Bug fixes and internal improvements

----

## New version 1.2

- Internal improvements and bug fixes

----

## New version 1.1

- Added -d; --directory option

----

## New version 1.0

- First stable release

----

Copyright (c) 2026 Hoang-Long2012
