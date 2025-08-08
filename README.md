```
usage: merge-files.py [-h] -i INPUTS [INPUTS ...] -o OUTPUT [-b BACKUP] [-id INPUTS_DIRECTORY] [-ie INPUT_EXTENSION] [-oe OUTPUT_EXTENSION] [-r REGEXES [REGEXES ...]]

options:
  -h, --help            show this help message and exit
  -i, --inputs INPUTS [INPUTS ...]
                        <Required> list of files to merge
  -o, --output OUTPUT   <Required> path to the output file
  -b, --backup BACKUP   path to backup directory
  -id, --inputs-directory INPUTS_DIRECTORY
                        if specified, all the inputs files are under this directory
  -ie, --input-extension INPUT_EXTENSION
                        if specified, input files must end with this extension
  -oe, --output-extension OUTPUT_EXTENSION
                        if specified, output path must end with this extension
  -r, --regexes REGEXES [REGEXES ...]
                        list of regexes to execute in order, all matches will be deleted from the output
```
