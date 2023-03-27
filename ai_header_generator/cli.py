import argparse
from .header_generator import MetaGenerator


def main():
    """ [insert]
    """    
    parser = argparse.ArgumentParser(description="AI-based metadata generator for code files.")

    parser.add_argument("--config", help="Path to the configuration file.", default="config.ini")

    parser.add_argument("--readme", help="Generate a README file based on the generated metadata.", action="store_true")

    parser.add_argument("--meta", help="re-run outdated template query results",optional=True, action="store_true", choices=['runall','refresh','delete'])

    parser.add_argument("--template", help="JSON template query.",optional=True)
    
    parser.add_argument("--file", help="Path to a specific code file to generate a metadata for.",optional=True)
    
    
    args = parser.parse_args()

    generator = MetaGenerator(config_file=args.config)
    
    if args.meta:
        if args.meta=="runall":
            generator.runall()
        if args.meta=="refresh":
            generator.refresh()
        if args.meta=="delete":
            generator.delete()
        exit(0)
    # Use the specified template if provided, otherwise use the default template
    try:
        if args.template:
            generator._read_template(file=args.template)
    except Exception as e:
        print("Error occurred while reading template file: ", e)
        exit(1)
    if args.file:
        generator.process_file(args.file)
    else:
        generator.process_files()
        
    if args.readme:
        generator.generate_readme()


if __name__ == "__main__":
    main()