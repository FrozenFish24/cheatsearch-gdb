# cheatsearch-gdb
A script to add CheatEngine style search commands to gdb

### Begin a new search with `cheatsearch new`:

`(gdb) cheatsearch new data-type start-address end-address value`

`data-type` may be one of the following
```
uint64 = unsigned 64 bit integer
sint64 = signed 64 bit integer
uint32 = unsigned 32 bit integer
sint32 = signed 32 bit integer
uint16 = unsigned 16 bit integer
sint16 = signed 16 bit integer
uint8  = unsigned 8 bit integer
sint8  = signed 8 bit integer
```
`value` can be omitted to search for an unknown initial value.

### Refine the search results with `cheatsearch next`:

`(gdb) cheatsearch next command`

`command` may be one of the following:
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
- Only little-endian integer types, no float or double support
- Memory is always dumped via `dump binary memory` to the cwd as `memory.bin`
