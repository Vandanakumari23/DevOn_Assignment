import pytest
from log_analyzer import LogAnalyzer

sample_logs = [
    "2023-03-01 08:15:27 - ServiceA - INFO - Started processing request #123",
    "2023-03-01 08:15:28 - ServiceB - ERROR - Null pointer exception",
    "2023-03-01 08:15:29 - ServiceA - INFO - Completed request #123 in 2ms",
    "2023-03-01 08:20:05 - ServiceC - WARN - Disk usage is at 85%",
    "2023-03-01 08:35:10 - ServiceB - ERROR - Null pointer exception",
    "2023-03-01 08:40:05 - ServiceA - INFO - Cleaned up temporary files",
    "2023-03-01 09:00:00 - ServiceB - INFO - Started job X",
    "2023-03-01 09:00:01 - ServiceB - ERROR - Job X failed to start",
    "2023-03-01 09:05:30 - ??? - INFO - Malformed line",
    "2023-03-01 09:10:00 - ServiceC - WARN - Low memory",
    "2023-03-01 - ServiceA - ERROR - Missing timestamp detail",
]

@pytest.fixture
def log_analyzer(tmp_path):
    """Fixture to create a LogAnalyzer instance with a sample log file."""
    log_file = tmp_path / "app.log"
    log_file.write_text("\n".join(sample_logs))
    analyzer = LogAnalyzer(log_file)
    return analyzer

def test_parse_log(log_analyzer):
    """Test that log entries are parsed correctly."""
    log_analyzer.parse_log()
    assert log_analyzer.log_levels_count['INFO'] == 4  
    assert log_analyzer.log_levels_count['ERROR'] == 3  
    assert log_analyzer.log_levels_count['WARN'] == 2   
    assert log_analyzer.service_count['ServiceA'] == 3  
    assert log_analyzer.service_count['ServiceB'] == 4  
    assert log_analyzer.service_count['ServiceC'] == 2  
    assert len(log_analyzer.malformed_lines) == 2 

def test_generate_summary(log_analyzer):
    """Test that the summary is generated correctly."""
    log_analyzer.parse_log()
    summary = log_analyzer.generate_summary()
    
    assert summary['log_levels_count']['INFO'] == 4
    assert summary['log_levels_count']['ERROR'] == 3
    assert summary['log_levels_count']['WARN'] == 2
    assert summary['service_count']['ServiceA'] == 3
    assert summary['most_common_error_message'] == "Null pointer exception"
    assert summary['most_common_error_count'] == 2
    assert summary['malformed_lines_count'] == 2
def test_malformed_line_handling(log_analyzer):
    """Test that malformed lines are handled gracefully."""
    log_analyzer.parse_log()
    assert len(log_analyzer.malformed_lines) == 2
if __name__ == "__main__":
    pytest.main()