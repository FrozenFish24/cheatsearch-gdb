# cheatsearch-gdb
A script to add CheatEngine style search commands to gdb

### Usage:
#### Begin a new search with `cheatsearch new`:

`(gdb) cheatsearch new start-address end-address value`

`value` can be omitted to search for an unknown initial value.

#### Change the state of the program then filter the results with `cheatsearch next` as required:

`(gdb) cheatsearch next command`

The command argument may be one of the following:
```
u  = Unchanged since last search
c  = Changed since last search
gt = Greater than last search
lt = Less than last search
nv = New value
```

if `nv` is specified, follow it with the new value:

`(gdb) cheatsearch next nv 1`

### Other commands:

Print the results of the last search:

`(gdb) cheatsearch results`

Clear the current search:

`(gdb) cheatsearch clear`

### Current Limitations:
- Only little-endian 32 bit integers are searchable
- Memory is always dumped via `dump binary memory` to the cwd as `memory.bin`
