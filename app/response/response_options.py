from field.predefined_types import PredefinedTypes as PT

RETURN_PARAMS = [
    PT.dict_number("rows",
                   "Wiersze",
                   "Ilość wygenerowanych wierszy.",
                   1,None,1),
    PT.dict_select("returned_type",
                   "Zwracany typ",
                   "Sposób, w jaki dane zostaną zwrócone.",
                   "json",
                   [
                       PT.dict_option("JSON", "json"),
                       PT.dict_option("plik CSV", "csv_file"),
                       PT.dict_option("plik JSON", "json_file"),
                       PT.dict_option("tabela HTML", "html_table")
                   ]
                   )]