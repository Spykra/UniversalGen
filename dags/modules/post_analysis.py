def generate_summary_report(data, report_path):
    """
    Generates a summary report from the analysis data.
    """
    with open(report_path, 'w') as f:
        summary = "Summary Report\n"
        summary += "---------------\n"

        for key, value in data.items():
            summary += f"{key}: {value}\n"
        f.write(summary)
    print(f"Summary report generated at {report_path}")
