
projects = [
    ("ScriptLanguages", "https://github.com/exasol/script-languages"),
    ("ScriptLanguagesRelease", "https://github.com/exasol/script-languages-release")
]


def get_project_names():
    return [project[0] for project in projects]


def get_project_url(project_name: str):
    match = [p[1] for p in projects if p[0] == project_name]
    assert len(match) == 1
    return match[0]
