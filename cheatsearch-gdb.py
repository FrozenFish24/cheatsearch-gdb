import gdb
import struct
from collections import namedtuple


Result = namedtuple('Result', ['file_addr', 'mem_addr', 'value'])
DataType = namedtuple('DataType', ['fmt', 'size'])


def first_search(needle, start_addr, data_type, filename):
    results = []

    with open(filename, 'rb') as f:
        f.seek(0, 2)
        file_size = f.tell()
        f.seek(0)

        while f.tell() < file_size:
            addr = f.tell()
            value = struct.unpack(data_type.fmt, f.read(data_type.size))[0]
            if value == needle:
                results.append(Result(addr, start_addr + addr, value))

    return results


def next_search(prev_results, command, data_type, filename, new_value=None):
    results = []

    with open(filename, 'rb') as f:
        for hit in prev_results:
            f.seek(hit.file_addr)
            value = struct.unpack(data_type.fmt, f.read(data_type.size))[0]

            match command:
                case 0:
                    if value == hit.value:
                        results.append(Result(hit.file_addr, hit.mem_addr, value))
                case 1:
                    if value != hit.value:
                        results.append(Result(hit.file_addr, hit.mem_addr, value))
                case 2:
                    if value > hit.value:
                        results.append(Result(hit.file_addr, hit.mem_addr, value))
                case 3:
                    if value < hit.value:
                        results.append(Result(hit.file_addr, hit.mem_addr, value))
                case 4:
                    if value == new_value:
                        results.append(Result(hit.file_addr, hit.mem_addr, value))
    return results


def print_results(results):
    if len(results) == 0:
        print(f'No results')
    elif len(results) == 1:
        print(f'{len(results)} result:')
    elif len(results) <= 10:
        print(f'{len(results)} results:')
    else:
        print(f'{len(results)} results, showing first 10:')

    for i in range(min(len(results), 10)):
        print(f'0x{results[i].mem_addr:08X} {results[i].value}')


class CheatSearch(gdb.Command):
    def __init__(self):
        super().__init__('cheatsearch', gdb.COMMAND_USER)
        self.start_addr = None
        self.end_addr = None
        self.searching = False
        self.results = None

    def invoke(self, arg, from_tty):
        args = gdb.string_to_argv(arg)

        if len(args) < 1:
            print('cheatsearch {new|next|results|clear} start-address end-address value {u,c,gt,lt,nv}')
            return

        match args[0]:
            case 'new':
                self.searching = True
                
                if args[1].startswith('0x') or args[1].startswith('0X'):
                    self.start_addr = int(args[1], 16)
                else:
                    self.start_addr = int(args[1])

                if args[2].startswith('0x') or args[2].startswith('0X'):
                    self.end_addr = int(args[2], 16)
                else:
                    self.end_addr = int(args[2])

                gdb.execute(f'dump binary memory memory.bin {self.start_addr} {self.end_addr}')
                self.results = first_search(int(args[3]), self.start_addr, DataType('<I', 4), 'memory.bin')
                print_results(self.results)
        
            case 'next':
                new_value = None
                match args[1]:
                    case 'u':           # Unchanged
                        command = 0
                    case 'c':           # Changed
                        command = 1
                    case 'gt':          # Greater than
                        command = 2
                    case 'lt':          # Less than
                        command = 3
                    case 'nv':          # New value
                        command = 4
                        new_value = int(args[2])
                        print(new_value)
                    case _:
                        return

                gdb.execute(f'dump binary memory memory.bin {self.start_addr} {self.end_addr}')
                print(new_value)
                self.results = next_search(self.results, command, DataType('<I', 4), 'memory.bin', new_value)
                print_results(self.results)

            case 'results':
                if not self.searching:
                    print("No search in progress.")
                else:
                    print_results(self.results)

            case 'clear':
                self.start = None
                self.end = None
                self.searching = False
                self.results = None


CheatSearch()