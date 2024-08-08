import argparse
import json


def load_config(args):
    with open(args.config, "r", encoding="utf8") as fh:
        config = json.load(fh)
    return config


def serialize_output(output):
    # serialize the output
    return json.dumps(output)


def run_version(args):
    from version import VERSION
    return {"version": VERSION}


def run(args, parser):
    # run the command
    if args.version:
        return run_version(args)

    parser.print_help()
    return None


def main():
    # parse arguments
    parser = argparse.ArgumentParser(
        prog='acdump',
        description='This is a tool to dump data from Active-Collab',
        epilog='(c) 2024 by ACME VC, Charlie Sloan <cs@example.com>')
    parser.add_argument('-v', '--version', action='store_true',
                        help="show version information for this tool", default=False)
    # parser.add_argument('-c', '--config', required=True,
    #                     help="use the named config file")

    args = parser.parse_args()
    output = run(args, parser)
    if output is not None:
        print(serialize_output(output))


if __name__ == "__main__":
    main()
