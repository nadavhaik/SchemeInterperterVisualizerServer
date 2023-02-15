from flask import Flask, request
from scheme_parser.ocaml_bridge import compile_parser

from scheme_parser.parser import ParsingMode, parse_scheme

app = Flask(__name__)


@app.route("/parse", methods=["POST"])
def parse():
    # return JSON to ajax call -- code input by user
    parsing_mode = ParsingMode[request.json['mode']]
    code = request.json['code']

    return parse_scheme(parsing_mode, code)


if __name__ == "__main__":
    compile_parser()

    app.run(debug=True)
