module.exports = {
    'root': true,

    'env': {
        'browser': true,
        'es2020': true
    },

    'parserOptions': {
        'ecmaVersion': 2020,
        'sourceType': 'module'
    },

    'rules': {
        // checks habilitados
        'brace-style': [
            'error',
            '1tbs'
        ],

        // https://google.github.io/styleguide/jsguide.html#features-arrays-trailing-comma
        // https://google.github.io/styleguide/jsguide.html#features-objects-use-trailing-comma
        'comma-dangle': [
            'error',
            'always-multiline'
        ],

        'curly': [
            'error',
            'multi-line',
            'consistent'
        ],
        
        'new-parens': 'error',
        'no-array-constructor': 'error',

        'no-console': [
            'error', {
                allow: [
                    'info',
                    'warn',
                    'error',
                    'assert'
                ]
            }
        ],

        'no-extra-boolean-cast': 'error',
        'no-extra-semi': 'error',
        'no-new-wrappers': 'error',

        'no-restricted-properties': [
            'error',
            {
                'property': '__lookupGetter__',
                'message': 'use Object.getOwnPropertyDescriptor'
            },

            {
                'property': '__lookupSetter__',
                'message': 'use Object.getOwnPropertyDescriptor'
            },

            {
                'property': '__defineGetter__',
                'message': 'use Object.defineProperty'
            },

            {
                'property': '__defineSetter__',
                'message': 'use Object.defineProperty'
            },

            {
                'object': 'cr',
                'property': 'exportPath',
                'message': 'use módulos es ou cr.define() em vez disso'
            }
        ],

        'no-throw-literal': 'error',
        'no-trailing-spaces': 'error',
        'no-var': 'error',
        'prefer-const': 'error',

        'quotes': [
            'error',
            'single', {
                allowTemplateLiterals: true
            }
        ],
        
        'semi': [
            'error',
            'always'
        ],

        // https://google.github.io/styleguide/jsguide.html#features-one-variable-per-declaration
        'one-var': [
            'error', {
                let: 'never',
                const: 'never'
            }
        ]
    },
    
    'overrides': [
        {
            'files': [
                '**/*.ts'
            ],

            'parser': './third_party/node/node_modules/@typescript-eslint/parser',

            'plugins': [
                '@typescript-eslint'
            ],

            'rules': {
                'no-unused-vars': 'off',

                '@typescript-eslint/no-unused-vars': [
                    'error', {
                        argsIgnorePattern: '^_',
                        varsIgnorePattern: '^_'
                    }
                ],

                'semi': 'off',

                '@typescript-eslint/semi': [
                    'error'
                ],

                // https://google.github.io/styleguide/tsguide.html#arrayt-type
                '@typescript-eslint/array-type': [
                    'error', {
                        default: 'array-simple'
                    }
                ],
            
                // https://google.github.io/styleguide/tsguide.html#type-assertions-syntax
                '@typescript-eslint/consistent-type-assertions': [
                    'error', {
                        assertionStyle: 'as'
                    }
                ],
            
                // https://google.github.io/styleguide/tsguide.html#interfaces-vs-type-aliases
                "@typescript-eslint/consistent-type-definitions": [
                    'error',
                    'interface'
                ],

                // https://google.github.io/styleguide/jsguide.html#naming
                '@typescript-eslint/naming-convention': [
                    'error',
                    {
                        selector: [
                            'class',
                            'interface',
                            'typeAlias',
                            'enum',
                            'typeParameter'
                        ],

                        format: [
                            'StrictPascalCase'
                        ],

                        filter: {
                            regex: '^(' +
                                'HTMLElementTagNameMap|HTMLElementEventMap' +
                                'HTML[A-Za-z]{0,}Element|' +
                                'UIEvent|UIEventInit|DOMError|' +
                                'WebUIListenerBehavior)$',

                            match: false
                        }
                    },

                    {
                        selector: 'enumMember',
                        format: ['UPPER_CASE']
                    },

                    {
                        selector: 'classMethod',
                        format: ['strictCamelCase'],
                        modifiers: ['public']
                    },
                    
                    {
                        selector: 'classMethod',
                        format: ['strictCamelCase'],
                        modifiers: ['private'],
                        trailingUnderscore: 'allow'
                    },

                    {
                        selector: 'classProperty',
                        format: ['UPPER_CASE'],
                        
                        modifiers: [
                            'private',
                            'static',
                            'readonly'
                        ]
                    },

                    {
                        selector: 'classProperty',
                        format: ['UPPER_CASE'],
                        
                        modifiers: [
                            'public',
                            'static',
                            'readonly'
                        ]
                    },

                    {
                        selector: 'classProperty',
                        format: ['camelCase'],
                        modifiers: ['public'],
                    },

                    {
                        selector: 'classProperty',
                        format: ['camelCase'],
                        modifiers: ['private'],
                        trailingUnderscore: 'allow'
                    },

                    {
                        selector: 'parameter',
                        format: ['camelCase'],
                        leadingUnderscore: 'allow'
                    },

                    {
                        selector: 'function',
                        format: ['camelCase']
                    }
                ],

                '@typescript-eslint/member-delimiter-style': [
                    'error', {
                        multiline: {
                            delimiter: 'comma',
                            requireLast: true
                        },
                        
                        singleline: {
                            delimiter: 'comma',
                            requireLast: false
                        },

                        overrides: {
                            interface: {
                                multiline: {
                                    delimiter: 'semi',
                                    requireLast: true
                                },

                                singleline: {
                                    delimiter: 'semi',
                                    requireLast: false
                                }
                            }
                        }
                    }
                ],

                // https://google.github.io/styleguide/tsguide.html#wrapper-types
                '@typescript-eslint/ban-types': [
                    'error', {
                        extendedDefaults: false,

                        types: {
                            String: {
                                message: 'use uma string em vez disso',
                                fixWith: 'string'
                            },

                            Boolean: {
                                message: 'use um boolean em vez disso',
                                fixWith: 'boolean'
                            },

                              Number: {
                                message: 'use um number em vez disso',
                                fixWith: 'number'
                            },

                            Symbol: {
                                message: 'use um symbol em vez disso',
                                fixWith: 'symbol'
                            },

                            BigInt: {
                                message: 'use um bigint em vez disso',
                                fixWith: 'bigint'
                            }
                        }
                    }
                ]
            }
        }
    ]
};