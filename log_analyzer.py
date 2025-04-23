import re
import json
from collections import defaultdict

class LogAnalyzer:
    def __init__(self, log_file):
        """
        Initializes the LogAnalyzer with the given log file.
        
        :param log_file: Path to the log file to analyze.
        """
        self.log_file = log_file
        self.log_levels_count = defaultdict(int)
        self.service_count = defaultdict(int)
        self.error_messages_count = defaultdict(int)
        self.malformed_lines = []

    def parse_log(self):
        """
        Reads the log file and parses each line to extract relevant information.
        Handles malformed lines by logging them.
        """
        log_pattern = re.compile(r'^(?P<timestamp>[\d\-]+\s[\d\:]+)\s-\s(?P<service_name>[\w]+)\s-\s(?P<log_level>[A-Z]+)\s-\s(?P<message>.+)$')
        
        with open(self.log_file, 'r') as file:
            for line in file:
                match = log_pattern.match(line.strip())
                if match:
                    self.process_log_entry(match.groupdict())
                else:
                    self.malformed_lines.append(line.strip())

    def process_log_entry(self, log_entry):
        """
        Processes a single log entry and aggregates counts.
        
        :param log_entry: A dictionary containing parsed log entry details.
        """
        timestamp = log_entry['timestamp']
        service_name = log_entry['service_name']
        log_level = log_entry['log_level']
        message = log_entry['message']
        # Update counts
        self.log_levels_count[log_level] += 1
        self.service_count[service_name] += 1
        
        # Count error messages specifically
        if log_level == 'ERROR':
            self.error_messages_count[message] += 1

    def generate_summary(self):
        """
        Generates a summary of the log analysis.
        
        :return: A summary dictionary containing counts and common error messages.
        """
        most_common_error = max(self.error_messages_count.items(), key=lambda x: x[1], default=(None, 0))
        summary = {
            'log_levels_count': dict(self.log_levels_count),
            'service_count': dict(self.service_count),
            'most_common_error_message': most_common_error[0],
            'most_common_error_count': most_common_error[1],
            'malformed_lines_count': len(self.malformed_lines)
        }
        return summary
    
    def print_summary(self):
        """
        Prints the summary in a readable format and saves it as a JSON file.
        """
        summary = self.generate_summary()
        
        # Print summary to console
        print(json.dumps(summary, indent=4))
        
        # Save summary to a JSON file
        with open('log_summary.json', 'w') as json_file:
            json.dump(summary, json_file, indent=4)
            print("Summary saved to log_summary.json")

def main():
    log_analyzer = LogAnalyzer('app.log')
    log_analyzer.parse_log()
    log_analyzer.print_summary()

if __name__ == "__main__":
    main()