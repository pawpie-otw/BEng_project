from pandas import DataFrame as DF

from fields.predefined_types import PredefinedTypes as PT

RESPONSES = [
    ("JSON", "json", None, "custom"),
    ("Plik CSV", "to_csv", DF.to_csv, "pandas"),
    ("Tabela HTML", "to_html", DF.to_html, "pandas"),
    ("Tabela LaTeX", "to_latex", DF.to_latex, "pandas")
]

RESPONSE_PARAMS = [
    PT.dict_number("rows",
                   "Wiersze",
                   "Ilość wygenerowanych wierszy.",
                   1, None, 1),
    PT.dict_select("returned_type",
                   "Zwracany typ",
                   "Sposób, w jaki dane zostaną zwrócone.",
                   [
                       PT.dict_option(repr, name)
                       for repr, name, *_ in RESPONSES
                   ]
                   )]

RESPONSES_FOR_CONVERTER = {name: {"method": method,
                                  "method_group": method_group}
                           for _, name, method, method_group in RESPONSES}
