"""
MAL-Toolbox Language Specification Module

"""

import logging
import json
import zipfile

logger = logging.getLogger(__name__)

def load_language_specification_from_mar(mar_archive: str) -> dict:
    """
    Read a ".mar" archive provided by malc (https://github.com/mal-lang/malc)
    and return a dictionary representing a MAL language structure

    Arguments:
    mar_archive     -   the path to a ".mar" archive

    Return:
    A dictionary representing the language specification
    """

    logger.debug(f'Load language specfication from \'{mar_archive}\' mar archive.')
    with zipfile.ZipFile(mar_archive, 'r') as archive:
        langspec = archive.read('langspec.json')
        return json.loads(langspec)

def load_language_specification_from_json(json_file: str) -> dict:
    """
    Read a MAL language JSON specification file

    Arguments:
    file_spec       - a language specification file that can be for example
                      provided by malc (https://github.com/mal-lang/malc)

    Return:
    A dictionary representing the language specification
    """

    logger.debug(f'Load language specfication from \'{json_file}\'.')
    with open(json_file, 'r', encoding='utf-8') as spec:
        data = spec.read()
    return json.loads(data)


def save_language_specification(lang_spec: dict, filename: str) -> dict:
    """
    Save a MAL language specification dictionary to a JSON file

    Arguments:
    lang_spec       - a dictionary containing the MAL language specification
    filename        - the JSON filename where the language specification will
                      be written
    """

    logger.debug(f'Save language specfication to {filename}.')

    lang = {}
    lang['name'] = lang_spec['defines']['id']
    lang['assets'] = get_attack_tree(lang_spec)
    lang['associations'] = []
    for assoc in lang_spec['associations']:
        del assoc['meta']
        lang['associations'].append(assoc)


    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(lang, file, indent=4)


def get_attacks_for_class(lang_spec: dict, asset_type: str) -> dict:
    """
    Get all Attack Steps for a specific Class

    Arguments:
    lang_spec       - a dictionary containing the MAL language specification
    asset_type      - a string representing the class for which we want to list
                      the possible attack steps

    Return:
    A dictionary representing the set of possible attacks for the specified
    class. Each key in the dictionary is an attack name and is associated
    with a dictionary containing other characteristics of the attack such as
    type of attack, TTC distribution, child attack steps and other information
    """
    attacks = {}
    asset = next((asset for asset in lang_spec['assets'] if asset['name'] == \
        asset_type), None)
    if not asset:
        logger.error(f'Failed to find asset type {asset_type} when '\
            'looking for attack steps.')
        return None

    if asset['superAsset']:
        attacks = get_attacks_for_class(lang_spec,
            asset['superAsset'])

    for attack in asset['attackSteps']:
        if attack['name'] not in attacks:
            attacks[attack['name']] = attack
        else:
            if attack['reaches']['overrides'] == True:
                attacks[attack['name']] = attack
            else:
                attacks[attack['name']]['reaches']['stepExpressions'].\
                    extend(attack['reaches']['stepExpressions'])

    return attacks


def get_variable_for_class_by_name(lang_spec: dict, asset_type: str,
    variable_name:str) -> dict:
    """
    Get a variables for a specific asset type by name.
    NOTE: Variables are the ones specified in MAL through `let` statements

    Arguments:
    lang_spec       - a dictionary containing the MAL language specification
    asset_type      - a string representing the type of asset which contains
                    the variable
    variable_name   - the name of the variable to search for

    Return:
    A dictionary representing the step expressions for the specified variable.
    """

    asset = next((asset for asset in lang_spec['assets'] if asset['name'] == \
        asset_type), None)
    if not asset:
        logger.error(f'Failed to find asset type {asset_type} when '\
            'looking for variable.')
        return None

    variable_dict = next((variable for variable in \
        asset['variables'] if variable['name'] == variable_name), None)
    if not variable_dict:
        logger.error(f'Failed to find variable {variable_name} in '\
            f'{asset_type}\'s language specification.')
        return None

    return variable_dict['stepExpression']
