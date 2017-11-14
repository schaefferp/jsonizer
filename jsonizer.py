#!/usr/bin/python
import json
import yaml
from os import path
from argparse import ArgumentParser

class jsonize(object):
    """ Opens, parses and creates yml or json from yml or json"""

    def __init__ (self):
        """ Main execution path """

        self._args = self._parse_cli_args()
        for input in self._args.input:
            self.process(input,self._args.output)

    @staticmethod
    def _parse_cli_args():
        """ Process command-line arguments """
 
        parser = ArgumentParser(prog='jsonizer', 
                                description="Translates either YAML to JSON"
                                " or JSON to YAML, depending on the input")
        parser.add_argument("input",
                            help="Input files to be processed",
                            nargs="+")
        parser.add_argument("--output",
                            help="Output path (default : same as input)",
                            nargs="?")
        return parser.parse_args()

    @staticmethod
    def process(input,output_path):
        """ Main method """
        is_yaml, is_json = False, False
        if input.lower().endswith("yml"):
            is_yaml = True
        elif input.lower().endswith("json"):
            is_json = True
        else:
            print "Skipping " + input + ", neither a YAML or JSON file,"
            " please use appropriate suffix."
            return(0)

        basepath, basename = path.split(input)
        filename = basename.rsplit(".",1)[0]

        if not output_path:
            output_path = basepath

        if is_yaml:
            with open(input) as raw:
                data = yaml.load(raw)
            
            output = path.join(output_path, filename + ".json")
            with open(output,"w") as output:
                json.dump(data, output)

        elif is_json:
            with open(input) as raw:
                data = json.load(raw)

            output = path.join(output_path, filename + ".yml")
            with open(output,"w") as output:
                yaml.safe_dump(data, output, encoding="utf-8", allow_unicode=True)


if __name__ == "__main__":
    try:
        jsonize()
    except RuntimeError as err:
        print >> sys.stderr, err
        exit(1)