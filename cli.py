import argparse
from ai_header_generator.header_generator import MetaGenerator


def main():

    parser = argparse.ArgumentParser(description="AI-based header generator for code files.")

    parser.add_argument("--config", help="Path to the configuration file.", default="config.ini")

    parser.add_argument("--readme", help="Generate a README file based on the generated headers.", action="store_true")

    args = parser.parse_args()

    generator = MetaGenerator(config_file=args.config)
    generator.process_files()


    if args.readme:
        generator.generate_readme()


if __name__ == "__main__":
    main()