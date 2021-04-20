"""Test (validate) language files."""
from src.glucolog.glucolog import list_languages, read_language_file


def _compare_dicts(it, it_dict, ot, ot_dict):
    """Compare presence of keys from both directions."""
    for field in it_dict.keys():
        assert field in ot_dict, "Field '%s' is missing from '%s' language file" % (
            field,
            ot,
        )
        if isinstance(it_dict[field], dict):
            _compare_dicts(it, it_dict[field], ot, ot_dict[field])

    for field in ot_dict.keys():
        assert field in it_dict, "Field '%s' is missing from '%s' language file" % (
            field,
            it,
        )
        if isinstance(it_dict[field], dict):
            _compare_dicts(it, it_dict[field], ot, ot_dict[field])


def test_language_files():
    """Confirm that language files are consistent."""
    # We use the "italian" file as the reference and confirm that all language
    # files contain all the same index keys in add sections.
    languages = list_languages()
    it_to, _it_from = read_language_file("it")
    for ot in languages:
        ot_to, _ot_from = read_language_file(ot)
        _compare_dicts("it", it_to, ot, ot_to)
