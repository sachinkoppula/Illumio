import csv
from collections import defaultdict

# Protocol number to name mapping
PROTOCOL_MAP = {
    "6": "tcp",
    "17": "udp",
    "1": "icmp"
}

# Load lookup table: Allow multiple tags per port/protocol combination
def load_lookup_table(lookup_file):
    lookup = defaultdict(list)
    with open(lookup_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            port = int(row[0].strip())
            protocol = row[1].strip().lower()  # Case-insensitive protocol
            tag = row[2].strip()
            lookup[(port, protocol)].append(tag)
    return lookup

# Parse and tag flow log data
def parse_and_tag_flow_logs(flow_log_file, lookup_table):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    untagged_count = 0

    with open(flow_log_file, 'r') as logfile:
        for line in logfile:
            fields = line.split()
            if len(fields) < 14:  # Ensure it is a valid flow log entry
                continue

            # Corrected field positions: destination port is in fields[5] and protocol is in fields[7]
            dst_port = int(fields[5].strip())
            protocol_number = fields[7].strip()
            protocol = PROTOCOL_MAP.get(protocol_number, "unknown")

            # Debugging: Check and print each port/protocol and its tag status
            tags = lookup_table.get((dst_port, protocol), ['Untagged'])
            if 'Untagged' in tags:
                untagged_count += 1
                print(f"No match for Port: {dst_port}, Protocol: {protocol}")
            else:
                for tag in tags:
                    print(f"Matched Tag '{tag}' for Port: {dst_port}, Protocol: {protocol}")
                    tag_counts[tag] += 1

            port_protocol_counts[(dst_port, protocol)] += 1

    # Add untagged count explicitly
    if untagged_count > 0:
        tag_counts['Untagged'] = untagged_count

    return tag_counts, port_protocol_counts

# Output results to files
def write_output(tag_counts, port_protocol_counts, tag_count_file, port_protocol_count_file):
    with open(tag_count_file, 'w') as outfile:
        outfile.write("Tag Counts:\n")
        outfile.write("Tag,Count\n")
        for tag, count in tag_counts.items():
            outfile.write(f"{tag},{count}\n")

    with open(port_protocol_count_file, 'w') as outfile:
        outfile.write("Port/Protocol Combination Counts:\n")
        outfile.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            outfile.write(f"{port},{protocol},{count}\n")

# Main function to execute the script
def main(flow_log_file, lookup_file, tag_count_file, port_protocol_count_file):
    lookup_table = load_lookup_table(lookup_file)
    tag_counts, port_protocol_counts = parse_and_tag_flow_logs(flow_log_file, lookup_table)
    write_output(tag_counts, port_protocol_counts, tag_count_file, port_protocol_count_file)

# Example usage
if __name__ == "__main__":
    main("flow_logs.txt", "lookup_table.csv", "tag_counts_output.csv", "port_protocol_counts_output.csv")
