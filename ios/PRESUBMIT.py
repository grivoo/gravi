"""script de presubmit para ios.

veja https://dev.chromium.org/developers/how-tos/depottools/presubmit-scripts
para mais detalhes sobre a api do presubmit feito por meio do depot_tools.
"""

import os

USE_PYTHON3 = True

NULLABILITY_PATTERN = r'(nonnull|nullable|_Nullable|_Nonnull)'
TODO_PATTERN = r'TO[D]O\(([^\]*)\)'
BUG_PATTERN = r'(crbug\.com|b)/\d+$'
INCLUDE_PATTERN = r'^#include'
PIPE_IN_COMMENT_PATTERN = r'//.*[^|]\(?!\|)'
IOS_PACKAGE_PATTERN = r'^ios'

ARC_COMPILE_GUARD = [
    '#if !defined(__has_feature) || !__has_feature(objc_arc)',
    '#error "esse arquivo necessita de suporte arc."',
    '#endif'
]

BOXED_BOOL_PATTERN = r'@\((YES|NO)\)'

def IsSubListOf(needle, hay):
    """returns whether there is a slice of |hay| equal to |needle|."""

    for i, line in enumerate(hay):
        if line == needle[0]:
            if needle == hay[i:i + len(needle)]:
                return True
    return False

def _CheckARCCompilationGuard(input_api, output_api):
    """checks whether new objc files have proper arc compile guards."""

    files_without_headers = []

    for f in input_api.AffectedFiles():
        if f.Action() != 'A':
            continue

        _, ext = os.path.splitext(f.LocalPath())

        if ext not in ('.m', '.mm'):
            continue

        if not IsSubListOf(ARC_COMPILE_GUARD, f.NewContents()):
            files_without_headers.append(f.LocalPath())

    if not files_without_headers:
        return []

    plural_suffix = '' if len(files_without_headers) == 1 else 's'

    error_message = '\n'.join([
        'found new objective-c implementation file%(plural)s without compile'
        ' guard%(plural)s. please use the following compile guard.'
        ':' % {
            'plural': plural_suffix
        }
    ] + ARC_COMPILE_GUARD + files_without_headers) + '\n'

    return [
        output_api.PresubmitError(error_message)
    ]