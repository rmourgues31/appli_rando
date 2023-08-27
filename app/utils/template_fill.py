from string import Template

def fill_template(template_file: str, variables: dict) -> str:
    '''
    Fill a template file with variables.
    '''

    with open(template_file, 'r', encoding="UTF8") as template:
        src = Template(template.read())
        result = src.substitute(variables)
    return result