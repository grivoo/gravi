"""script para presubmit de alto-nível para o gravi.

veja https://www.chromium.org/developers/how-tos/depottools/presubmit-scripts/
para mais detalhes sobre a api do presubmit feita pelo depot_tools.
"""

# imports
from typing import Callable
from typing import Optional
from typing import Sequence

from dataclasses import dataclass

PRESUBMIT_VERSION = "2.0.0"

USE_PYTHON3 = True

_EXCLUDED_PATHS = (
    # arquivo gerado
    (r"chrome/android/webapk/shell_apk/src/org/chromium"
     r"/webapk/lib/runtime_library/IWebApkApi.java"),

    # :P
    r"chrome/updater/mac/keystone/ksadmin.mm",

    # arquivo gerado
    (r"^components/variations/proto/devtools/"
     r"client_variations.js"),

    # arquivos de vídeos, não typescript
    r"^media/test/data/.*.ts",
    r"^native_client_sdksrc/build_tools/make_rules.py",
    r"^native_client_sdk/src/build_tools/make_simple.py",
    r"^native_client_sdk/src/tools/.*.mk",
    r"^net/tools/spdyshark/.*",
    r"^skia/.*",
    r"^third_party/blink/.*",
    r"^third_party/breakpad/.*",

    # sqlite é uma dependência third party importada
    r"^third_party/sqlite/.*",
    r"^v8/.*",
    r".*MakeFile$",
    r".+_autogen\.h$",
    r".+_pb2(_grpc)?\.py$",
    r".+/pnacl_shim\.c$",
    r"^gpu/config/.*_list_json\.cc$",
    r"tools/md_browser/.*\.css$",

    # páginas de teste para testes de telemetry maps
    r"tools/perf/page_sets/maps_perf_test.*",

    # páginas de teste para testes de telemetry webrtc
    r"tools/perf/page_sets/webrtc_cases.*"
)

_EXCLUDED_SET_NO_PARENT_PATHS = (
    'third_party/blink/OWNERS'
)

_IMPLEMENTATION_EXTENSIONS = r'\.(cc|cpp|cxx|mm)$'
_HEADER_EXTENSIONS = r'\.(h|hpp|hxx)$'

_NON_BASE_DEPENDENT_PATHS = (
    r"^chrome/browser/browser_switcher/bho/",
    r"^tools/win/"
)

_TEST_CODE_EXCLUDED_PATHS = (
    r'.*/(fake_|test_|mock_).+%s' % _IMPLEMENTATION_EXTENSIONS,
    r'.+_test_(base|support|util)%s' % _IMPLEMENTATION_EXTENSIONS,
    r'.+_(api|browser|eg|int|perf|pixel|unit|ui)?test(s)?(_[a-z]+)?%s' %
        _IMPLEMENTATION_EXTENSIONS,
    r'.+_(fuzz|fuzzer)(_[a-z]+)?%s' % _IMPLEMENTATION_EXTENSIONS,
    r'.+sync_service_impl_harness%s' % _IMPLEMENTATION_EXTENSIONS,
    r'.*/(test|tool(s)?)/.*',

    # content_shell is used for running content_browsertests.
    r'content/shell/.*',

    # Web test harness.
    r'content/web_test/.*',

    # Non-production example code.
    r'mojo/examples/.*',

    # Launcher for running iOS tests on the simulator.
    r'testing/iossim/iossim\.mm$',

    # EarlGrey app side code for tests.
    r'ios/.*_app_interface\.mm$',

    # códigos de exemplos para views
    r'ui/views/examples/.*',

    # codelab do gravi
    r'codelabs/*'
)

_THIRD_PARTY_EXCEPT_BLINK = 'third_party/(?!blink/)'

_TEST_ONLY_WARNING = (
    'you might be calling functions intended only for testing from\n'
    'production code. if you are doing this from inside another method\n'
    'named as *ForTesting(), then consider exposing things to have tests\n'
    'make that same call directly.\n'
    'if that is not possible, you may put a comment on the same line with\n'
    '  // IN-TEST \n'
    'to tell the PRESUBMIT script that the code is inside a *ForTesting()\n'
    'method and can be ignored. do not do this inside production code.\n'
    'the android-binary-size trybot will block if the method exists in the\n'
    'release apk.')

@dataclass
class BanRule:
    pattern: str
    explanation: Sequence[str]
    treat_as_error: Optional[bool] = None
    excluded_paths: Optional[Sequence[str]] = None

_BANNED_JAVA_IMPORTS : Sequence[BanRule] = (
    BanRule(
        'import java.net.URI;',
        (
            'use org.chromium.url.GURL instead of java.net.URI, where possible.'
        ),

        excluded_paths=(
            (r'net/android/javatests/src/org/chromium/net/'
            'AndroidProxySelectorTest\.java'),
            r'components/cronet/',
            r'third_party/robolectric/local/'
        )
    ),

    BanRule(
        'import android.annotation.TargetApi;',
        (
            'do not use TargetApi, use @androidx.annotation.RequiresApi instead. '
            'RequiresApi ensures that any calls are guarded by the appropriate '
            'SDK_INT check. see https://crbug.com/1116486.'
        )
    ),

    BanRule(
        'import android.support.test.rule.UiThreadTestRule;',
        (
            'do not use UiThreadTestRule, just use '
            '@org.chromium.base.test.UiThreadTest on test methods that should run '
            'on the ui thread. see https://crbug.com/1111893.'
        )
    ),

    BanRule(
        'import android.support.test.annotation.UiThreadTest;',
        ('do not use android.support.test.annotation.UiThreadTest, use '
        'org.chromium.base.test.UiThreadTest instead. see '
        'https://crbug.com/1111893.'
        )
    ),

    BanRule(
        'import android.support.test.rule.ActivityTestRule;',
        (
            'do not use ActivityTestRule, use '
            'org.chromium.base.test.BaseActivityTestRule instead.'
        ),

        excluded_paths=(
            'components/cronet/'
        )
    ),

    BanRule(
        'import androidx.vectordrawable.graphics.drawable.VectorDrawableCompat;',
        (
            'do not use VectorDrawableCompat, use getResources().getDrawable() to '
            'avoid extra indirections. please also add trace event as the call '
            'might take more than 20 ms to complete.'
        )
    )
)

_BANNED_JAVA_FUNCTIONS : Sequence[BanRule] = (
    BanRule(
      'StrictMode.allowThreadDiskReads()',
      (
       'Prefer using StrictModeContext.allowDiskReads() to using StrictMode '
       'directly.',
      ),
      False,
    ),
    BanRule(
      'StrictMode.allowThreadDiskWrites()',
      (
       'Prefer using StrictModeContext.allowDiskWrites() to using StrictMode '
       'directly.',
      ),
      False,
    ),
    BanRule(
      '.waitForIdleSync()',
      (
       'Do not use waitForIdleSync as it masks underlying issues. There is '
       'almost always something else you should wait on instead.',
      ),
      False,
    ),

    BanRule(
      r'/(?<!\bsuper\.)(?<!\bIntent )\bregisterReceiver\(',
      (
       'Do not call android.content.Context.registerReceiver (or an override) '
       'directly. Use one of the wrapper methods defined in '
       'org.chromium.base.ContextUtils, such as '
       'registerProtectedBroadcastReceiver, '
       'registerExportedBroadcastReceiver, or '
       'registerNonExportedBroadcastReceiver. See their documentation for '
       'which one to use.',
      ),
      True,
      excluded_paths=(
          r'.*Test[^a-z]',
          r'third_party/',
          'base/android/java/src/org/chromium/base/ContextUtils.java',
          'chromecast/browser/android/apk/src/org/chromium/chromecast/shell/BroadcastReceiverScope.java',
      ),
    ),

    BanRule(
        r'/(?:extends|new)\s*(?:android.util.)?Property<[A-Za-z.]+,\s*(?:Integer|Float)>',
        (
            'do not use Property<..., Integer|Float>, but use FloatProperty or '
            'IntProperty because it will avoid unnecessary autoboxing of '
            'primitives.'
        )
    ),

    BanRule(
        'requestLayout()',
        (
            'layouts can be expensive. prefer using ViewUtils.requestLayout(), '
            'which emits a trace event with additional information to help with '
            'scroll jank investigations. see http://crbug.com/1354176.'
        ),
        
        False,

        excluded_paths=(
            'ui/android/java/src/org/chromium/ui/base/ViewUtils.java'
        ),
    ),

    BanRule(
        'Profile.getLastUsedRegularProfile()',
        (
            'prefer passing in the profile reference instead of relying on the '
            'static getLastUsedRegularProfile() call. only top level entry points '
            '(e.g. Activities) should call this method. otherwise, the profile '
            'should either be passed in explicitly or retreived from an existing '
            'entity with a reference to the profile (e.g. WebContents).'
        ),
        
        False,
        
        excluded_paths=(
            r'.*Test[A-Z]?.*\.java'
        )
    ),

    BanRule(
        r'/(ResourcesCompat|getResources\(\))\.getDrawable\(\)',

        (
            'getDrawable() can be expensive. if you have a lot of calls to '
            'GetDrawable() or your code may introduce janks, please put your calls '
            'inside a trace().'
        ),
        
        False,

        excluded_paths=(
            r'.*Test[A-Z]?.*\.java'
        )
    ),

    BanRule(
        r'/RecordHistogram\.getHistogram(ValueCount|TotalCount|Samples)ForTesting\(',
        (
            'raw histogram counts are easy to misuse; for example they don\'t reset '
            'between batched tests. use HistogramWatcher to check histogram records instead.'
        ),
        
        False,

        excluded_paths=(
            'base/android/javatests/src/org/chromium/base/metrics/RecordHistogramTest.java',
            'base/test/android/javatests/src/org/chromium/base/test/util/HistogramWatcher.java'
        )
    )
)