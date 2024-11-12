# Flow Log Tagging Program

## Assumptions:
1. The program only supports the default AWS Flow Log format (version 2).
2. The flow log file should be in plain text (ASCII) format.
3. The lookup table should map `dstport` and `protocol` to tags.
4. The flow log file size can be up to 10 MB.
5. The lookup table file can have up to 10,000 mappings.
6. Tags can map to more than one port/protocol combination.
7. Protocols and tags are compared in a case-insensitive manner.

## Features:
- **Efficient handling of large flow log files** by reading the file line by line.
- **Case-insensitive matching** for port and protocol.
- **Support for multiple tags per port/protocol combination**.
- **Generates output files** with tag counts and port/protocol combination counts.

## Instructions:
1. Run the program using the following command:
    ```bash
    python flow_log_tagging.py flow_logs.txt lookup_table.csv tag_counts_output.csv port_protocol_counts_output.csv
    ```
    - `flow_logs.txt`: The input flow log file.
    - `lookup_table.csv`: The lookup table mapping ports and protocols to tags.
    - `tag_counts_output.csv`: The output file containing tag counts.
    - `port_protocol_counts_output.csv`: The output file containing port/protocol combination counts.

## Tests:
- **Basic Test**: Ran the program with a small sample `flow_logs.txt` and a corresponding `lookup_table.csv`. The program correctly tagged the entries and produced the expected output files.
- **Large File Test**: Successfully handled a flow log file of size ~7 MB without running into memory issues.
- **Case-Insensitive Test**: Verified that protocol matching works regardless of case (e.g., 'TCP' vs 'tcp').

## Future Improvements:
- The lookup table can be extended to handle more edge cases, such as custom ports or additional protocols.
- The program could be optimized further for even larger files if needed (e.g., using parallel processing for multiple core systems).
