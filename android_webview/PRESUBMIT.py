"""testes de presubmit para //android_webview/

gates contra o uso da api Context#bindService antes do upload.
"""

USE_PYTHON3 = True


def CheckChangeOnCommit(input_api, output_api):
    results = []

    results.extend(_CheckNoContextBindServiceAdded(input_api, output_api))

    return results

def CheckChangeOnUpload(input_api, output_api):
    results = []

    results.extend(_CheckNoContextBindServiceAdded(input_api, output_api))

    return results

def _CheckNoContextBindServiceAdded(input_api, output_api):
    """verifica se nenhum arquivo novo em //android_webview usa diretamente o
    Context#bindService. isso ocorre porque a plataforma android não permite chamadas
    Context#bindService() de dentro de um contexto BroadcastReceiver.
    """

    errors = []

    bind_service_pattern = input_api.re.compile(
        r'.*\.bindService\(.*)'

    def _FilterFile(affected_file):
        skip_files = (input_api.DEFAULT_FILES_TO_SKIP +
            (r'.*android_webview[/\\]common[/\\]services[/\\]ServiceHelper\.java',
                r'.*android_webview[/\\]support_library[/\\]boundary_interfaces[/\\].*',
                r'.*android_webview[/\\]js_sandbox[/\\].*'))

        return input_api.FilterSourceFile(
            affected_file,

            files_to_skip = skip_files,
            files_to_check = [r'.+\.java$']
        )
    )

    for f in input_api.AffectedSourceFiles(_FilterFile):
        for line_num, line in f.ChangedContents():
            match = bind_service_pattern.search(line)

            if match:
                if "ServiceHelper.bindService" not in line:
                    errors.append("%s:%d:%s" % (f.LocalPath(), line_num, line))

    results = []

    if errors:
        results.append(output_api.PresubmitPromptWarning("""
novo código em //android_webview não deve user \
android.content.Context#bindService. em vez disso, use \
android_webview.common.services.ServiceHelper#bindService.
""", errors))

return results