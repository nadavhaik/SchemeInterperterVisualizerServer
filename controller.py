from flask import Flask, request
from flask_cors import CORS
from scheme_parser.ocaml_bridge import compile_parser

from scheme_parser.parser import ParsingMode, parse_scheme

app = Flask(__name__)
CORS(app)


@app.route("/parse", methods=["POST"])
def parse():
    # return JSON to ajax call -- code input by user
    print(f'got: {request.json}')
    parsing_mode = ParsingMode[request.json['mode']]
    code = request.json['code']
    result = parse_scheme(parsing_mode, code)
    return result


if __name__ == "__main__":
    compile_parser()

    app.run(debug=True)
