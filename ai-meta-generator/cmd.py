import argparse
try:
    from .main import ExecuteClass
except ImportError:
    from main import ExecuteClass
    
def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="AI-based header generator for code files.")
    parser.add_argument("--config", help="Path to the configuration file.", default="config.ini")
    parser.add_argument("--meta", help="re-run outdated template query results", action="store", choices=['runall', 'init', 'refresh', 'delete'])
    parser.add_argument("--template", help="JSON template query.")
    parser.add_argument("--file", help="Path to a specific code file to generate a header for.")
    parser.add_argument("--max", help="Max files per template file", default=50)
    args = parser.parse_args()

    execu = ExecuteClass(args)
    execu.run()

if __name__ == "__main__":
    main()
