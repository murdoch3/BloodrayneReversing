# Bloodrayne uses POD3 archive files to store game files
# This script can be used to extract them 

import struct


################################################################################
# Utility functions

def read_c_string(data, offset, max_length):
    i = offset
    while i < len(data) and i - offset < max_length and data[i] != 0:
        i += 1
    return data[offset:i].decode(encoding='ascii')

################################################################################


################################################################################
# Structs

# Header format 
# struct header
# {
# /* 0x0000 */  c8<4> ident;        // AKA magic
# /* 0x0004 */ u32<1> checksum;     
# /* 0x0008 */ c8<80> comment; 
# /* 0x0058 */ u32<1> entry_count;  // AKA file_count 
# /* 0x005c */ u32<1> audit_count;  // AKA audit_file_count
# /* 0x0060 */ u32<1> revision;
# /* 0x0064 */ u32<1> priority;
# /* 0x0068 */ c8<80> author;
# /* 0x00B8 */ c8<80> copyright;
# /* 0x0108 */ u32<1> entry_offset; // index_offset
# /* 0x010c */ u32<1> entry_crc;
# /* 0x0110 */ u32<1> names_size;
# /* 0x0114 */ u32<1> depends_count;
# /* 0x0118 */ u32<1> depends_crc;
# /* 0x011c */ u32<1> audits_crc;
# }

HEADER_FORMAT = "<4s I 80s I I I I 80s 80s I I I I I I"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
HEADER_TITLES = [
    "ident",   
    "checksum",
    "comment", 
    "entry_count",
    "audit_count",
    "revision",
    "priority",
    "author",
    "copyright",
    "entry_offset",
    "entry_crc",
    "names_size",
    "depends_count",
    "depends_crc",
    "audits_crc"
]

# struct entry
# {
#         u32<1> name_offset;   // AKA file_path_offset 
#         u32<1> size;          // AKA file_size 
#         u32<1> offset;        // AKA file_offset 
#         t32<1> timestamp;     // AKA file_timestamp
#         u32<1> checksum;      // AKA file_checksum
# };
ENTRY_FORMAT = "<I I I I I"
ENTRY_SIZE = struct.calcsize(ENTRY_FORMAT)
ENTRY_TITLES = [
    "name_offset",
    "size",
    "offset",
    "timestamp",
    "checksum"
]

################################################################################

def read_header(data):
    raw_header = struct.unpack(HEADER_FORMAT, data[:HEADER_SIZE])
    header = {}
    for i in range(len(raw_header)):
        header[HEADER_TITLES[i]] = raw_header[i]
    return header

# TODO: Confirm that this is actually the names section
# This seems to happen between the header and the entries 
# Doesn't seem to happen in every file 
# After reviewing, I think this might be data that each entry refers back to
def read_strings(data, entry_offset):
    x = data[HEADER_SIZE:entry_offset]
    return x.split(b'\x0D\x0A')

# Read the entry at the current offset
def read_entry(data, offset):
    raw_entry = struct.unpack(ENTRY_FORMAT, data[offset:offset+ENTRY_SIZE])
    entry = {}
    for i in range(len(raw_entry)):
        entry[ENTRY_TITLES[i]] = raw_entry[i]
    return entry

def read_entries(data, entry_offset, entry_count):
    entries = []
    for i in range(entry_count):
        entry = read_entry(data, entry_offset + i*ENTRY_SIZE)
        entries.append(entry)
    return entries 

def get_entry_filename(data, header, entry):
    #pod_file.seek(self.index_offset + (self.file_count * DIR_ENTRY_SIZE) + metadata["path_offset"])
    #file_name = self._get_c_string(pod_file.read(FILE_NAME_LENGTH))
    # start is at 
    filename_start = header["entry_offset"] + header["entry_count"]*ENTRY_SIZE + entry["name_offset"]
    filename_length = 256 # not sure how we know this ... 
    # data[filename_start:filename_start+filename_length]
    print(read_c_string(data, filename_start, filename_length))


with open('C:/Users/murdoch/Downloads/BloodRayne (USA)/BloodRayne (USA)/english.pod', 'rb') as f:
    data = f.read()

header = read_header(data)
print(header)
#print(len(read_strings(data, header["entry_offset"])))
entries = read_entries(data, header['entry_offset'], header['entry_count'])
for entry in entries:
    get_entry_filename(data, header, entry)