#!/usr/bin/env python3
"""
Flutter Test Generator — Generates test boilerplate from Clean Architecture source files.

Usage:
    python3 generate_test.py apps/mobile/lib/features/auth/domain/usecases/sign_in.dart
    python3 generate_test.py lib/features/profile/data/models/user_profile_model.dart
"""

import sys
import os
import re
from pathlib import Path
from typing import Optional

NL = chr(10)


def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()


def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def find_pubspec_dir(path: str) -> Optional[str]:
    current = os.path.dirname(os.path.abspath(path))
    while True:
        if os.path.exists(os.path.join(current, 'pubspec.yaml')):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def get_package_name(pubspec_dir: str) -> str:
    pubspec_path = os.path.join(pubspec_dir, 'pubspec.yaml')
    if os.path.exists(pubspec_path):
        content = read_file(pubspec_path)
        match = re.search(r'^name:\s+(\S+)', content, re.MULTILINE)
        if match:
            return match.group(1)
    return 'mobile'


def detect_layer(filepath: str) -> str:
    path = filepath.replace('\\', '/').lower()
    if '/core/' in path:
        if '/network/' in path:
            return 'core_network'
        elif '/services/' in path:
            return 'core_service'
        elif '/error/' in path:
            return 'core_error'
        elif '/widgets/' in path:
            return 'core_widget'
        else:
            return 'core_generic'

    if '/presentation/cubit/' in path and path.rstrip('_').endswith('_state.dart'):
        return 'presentation_state'
    if '/presentation/cubit/' in path:
        return 'presentation_cubit'
    if '/presentation/pages/' in path:
        return 'presentation_page'
    if '/presentation/widgets/' in path:
        return 'presentation_widget'
    if '/domain/entities/' in path:
        return 'domain_entity'
    if '/domain/usecases/' in path:
        return 'domain_usecase'
    if '/data/models/' in path:
        return 'data_model'
    if '/data/datasources/' in path:
        return 'data_datasource'
    if '/data/repositories/' in path:
        return 'data_repository'

    return 'unknown'


def get_test_path(source_path: str) -> str:
    path = source_path.replace('\\', '/')
    base, ext = os.path.splitext(path)
    test_path = re.sub(r'/lib/', '/test/', f'{base}_test{ext}', count=1)
    return test_path


def capitalize(s: str) -> str:
    return s[0].upper() + s[1:] if s else s


def split_camel(name: str) -> str:
    parts = re.findall(r'[A-Z]?[a-z0-9]+|[A-Z]+(?=[A-Z]|$)', name)
    return '_'.join(p.lower() for p in parts)


def extract_ctor_params(content: str, class_name: str) -> list:
    clean = re.sub(r'//.*', '', content)
    clean = re.sub(r'/\*.*?\*/', '', clean, flags=re.DOTALL)

    fields = {}
    for m in re.finditer(r'final\s+([\w<>,\s?]+?)\s+(\w+)\s*;', clean):
        type_name = re.sub(r'\s+', ' ', m.group(1).strip())
        fields[m.group(2)] = type_name

    ctor_match = re.search(rf'{class_name}\s*\((.*?)\)', clean, re.DOTALL)
    if not ctor_match:
        return []

    params_str = ctor_match.group(1)

    param_names = re.findall(r'this\.(\w+)', params_str)
    if not param_names:
        for m in re.finditer(r'(?:required\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)\s*(?:,|\))', params_str):
            param_type = m.group(1).strip()
            param_name = m.group(2).strip()
            if param_type != class_name and not param_type[0].isupper():
                continue
            if param_name == class_name:
                continue
            param_names.append(param_name)
            if param_name not in fields:
                fields[param_name] = param_type

    result = []
    for name in param_names:
        type_name = fields.get(name, 'dynamic')
        if type_name == class_name:
            continue
        result.append({'name': name, 'type': type_name})
    return result


SKIP_METHODS = {'catch', 'if', 'for', 'while', 'switch', 'return', 'throw', 'on'}


def extract_methods(content: str, class_name: str) -> list:
    clean = re.sub(r'//.*', '', content)
    clean = re.sub(r'/\*.*?\*/', '', clean, flags=re.DOTALL)

    methods = []
    pattern = r'([\w<>?,\s]+?)\s+(\w+)\s*\(([^)]*)\)\s*(?:async\s*)?\{'
    for m in re.finditer(pattern, clean):
        ret_type = m.group(1).strip()
        method_name = m.group(2).strip()
        if method_name == class_name or method_name.startswith('_') or method_name in SKIP_METHODS:
            continue
        params_str = m.group(3).strip()
        methods.append({
            'name': method_name,
            'return_type': ret_type,
            'params_str': params_str,
        })
    return methods


def parse_dart_file(filepath: str, pubspec_dir: str) -> dict:
    content = read_file(filepath)
    clean = re.sub(r'//.*', '', content)
    clean = re.sub(r'/\*.*?\*/', '', clean, flags=re.DOTALL)

    class_match = re.search(
        r'class\s+(\w+)(?:\s+extends\s+([^{]+?))?(?:\s+implements\s+([^{]+?))?\s*\{',
        clean,
    )
    if not class_match:
        raise ValueError(f"No class found in {filepath}")

    class_name = class_match.group(1)
    extends = class_match.group(2).strip() if class_match.group(2) else None
    implements = class_match.group(3).strip() if class_match.group(3) else None

    file_name = os.path.splitext(os.path.basename(filepath))[0]

    abs_path = os.path.abspath(filepath)
    lib_dir = os.path.join(pubspec_dir, 'lib')
    try:
        rel_path = os.path.relpath(abs_path, lib_dir)
    except ValueError:
        rel_path = ''

    path_parts = rel_path.replace('\\', '/').split('/')

    feature = None
    if 'features' in path_parts:
        feat_idx = path_parts.index('features')
        if len(path_parts) > feat_idx + 1:
            feature = path_parts[feat_idx + 1]

    has_either = 'Either<' in content
    is_cubit = extends and 'Cubit' in extends if extends else False
    is_part_of = 'part of' in content

    pkg = get_package_name(pubspec_dir)
    pkg_base = rel_path.replace('\\', '/')
    pkg_import = f"package:{pkg}/{pkg_base}"

    imports = re.findall(r"import\s+'([^']+)';", content)
    package_imports = [i for i in imports if i.startswith('package:')]

    deps = extract_ctor_params(content, class_name)
    methods = extract_methods(content, class_name)

    return {
        'class_name': class_name,
        'extends': extends,
        'implements': implements,
        'file_name': file_name,
        'feature': feature,
        'has_either': has_either,
        'is_cubit': is_cubit,
        'is_part_of': is_part_of,
        'pkg_import': pkg_import,
        'pkg': pkg,
        'imports': package_imports,
        'dependencies': deps,
        'methods': methods,
        'rel_path': pkg_base,
        'content': content,
    }


def build_test_imports(info: dict, layer: str) -> list:
    result = ['package:flutter_test/flutter_test.dart']

    if layer in ('presentation_cubit', 'presentation_state'):
        result.append('package:bloc_test/bloc_test.dart')
        result.append('dart:async')

    if info['has_either'] and layer in ('domain_usecase', 'data_repository'):
        result.append('package:fpdart/fpdart.dart')

    has_mocks = layer in (
        'domain_usecase', 'data_datasource', 'data_repository',
        'presentation_cubit', 'presentation_page', 'presentation_widget',
        'core_network', 'core_service',
    )
    if has_mocks and 'package:mocktail/mocktail.dart' not in result:
        result.append('package:mocktail/mocktail.dart')

    if layer == 'data_model':
        result.append('dart:convert')
        result.append('dart:io')

    for imp in info['imports']:
        if imp not in result:
            include = False
            if '/core/' in imp:
                include = True
            elif '/features/' in imp:
                dep_types = [d['type'].split('<')[0].strip() for d in info['dependencies']]
                for dt in dep_types:
                    if dt.lower().replace('_', '') in imp.lower():
                        include = True
                        break
            if include:
                result.append(imp)

    pkg_import = info['pkg_import']
    parent_import = None
    if info['is_part_of']:
        parent_import = re.sub(r'_(state|event)\.dart$', r'_\1.dart', pkg_import)
        parent_import2 = re.sub(r'_(state|event)\.dart$', '.dart', pkg_import)
        if 'cubit' in parent_import2:
            parent_import = parent_import2
        elif 'bloc' in parent_import2:
            parent_import = parent_import2

    import_target = parent_import if info['is_part_of'] and parent_import else pkg_import
    if import_target not in result:
        result.append(import_target)

    if info['has_either'] and layer in ('domain_usecase', 'data_repository'):
        has_failures = any('failures.dart' in i for i in result)
        if not has_failures:
            result.append(f'package:{info["pkg"]}/core/error/failures.dart')

    return result


def get_helpers_import(info: dict) -> str:
    rel = info['rel_path']
    depth = rel.count('/') - 1
    prefix = '../' * max(depth, 1)
    return f"import '{prefix}helpers/fixture_reader.dart';"


def format_imports(imports: list) -> str:
    framework = []
    dart = []
    core = []
    feature = []
    other = []

    for i in imports:
        if i.startswith('package:flutter_test'):
            if not framework:
                framework.append(i)
        elif i.startswith('package:bloc_test'):
            if 'package:bloc_test' not in framework:
                framework.append(i)
        elif i.startswith('package:fpdart'):
            if 'package:fpdart' not in framework:
                framework.append(i)
        elif i.startswith('package:mocktail'):
            if 'package:mocktail' not in framework:
                framework.append(i)
        elif i.startswith('dart:'):
            dart.append(i)
        elif '/core/' in i:
            core.append(i)
        elif '/features/' in i:
            feature.append(i)
        else:
            other.append(i)

    lines = []
    for f in framework:
        lines.append(f"import '{f}';")
    if dart:
        lines.append('')
        for d in dart:
            lines.append(f"import '{d}';")
    if core:
        lines.append('')
        for c in core:
            lines.append(f"import '{c}';")
    if feature:
        lines.append('')
        for f in feature:
            lines.append(f"import '{f}';")
    if other:
        lines.append('')
        for o in other:
            lines.append(f"import '{o}';")
    lines.append('')
    return NL.join(lines)


def mock_name(type_name: str) -> str:
    clean = type_name.split('<')[0].strip()
    if not clean.startswith('Mock'):
        return f'Mock{clean}'
    return clean


def generate_mocks(info: dict, layer: str) -> str:
    if layer in ('domain_entity', 'data_model', 'presentation_state', 'core_error'):
        return ''
    deps = info['dependencies']
    if not deps:
        return ''
    seen = set()
    lines = []
    for dep in deps:
        dt = dep['type']
        if dt == 'dynamic' or dt in seen:
            continue
        seen.add(dt)
        lines.append(f'class {mock_name(dt)} extends Mock implements {dt} {{}}')
    return NL.join(lines)


def var_name(dep_name: str) -> str:
    return f'mock{dep_name[0].upper()}{dep_name[1:]}'


# ──────────────────────────── TEMPLATES ────────────────────────────


def template_entity(info: dict) -> str:
    cn = info['class_name']
    fields = [d['name'] for d in info['dependencies']]
    fields_str = ', '.join(fields) if fields else '...'
    raw = (
        format_imports(build_test_imports(info, 'domain_entity'))
        + NL
        + f"""void main() {{
  group('{cn}', () {{
    group('Equatable', () {{
      test('debería ser igual cuando todos los campos son los mismos', () {{
        // ARRANGE: crear dos instancias con los mismos valores
        // ACT: comparar con ==
        // ASSERT: expect(instance1, equals(instance2))
      }});

      test('debería ser diferente cuando algún campo cambia', () {{
        // ARRANGE: crear dos instancias con valores distintos
        // ACT: comparar con ==
        // ASSERT: expect(instance1, isNot(equals(instance2)))
      }});
    }});

    group('copyWith', () {{
      test('debería actualizar solo el campo especificado', () {{
        // ARRANGE: crear instancia original
        // ACT: llamar copyWith(campo: nuevoValor)
        // ASSERT: verificar que el campo cambió y los demás no
      }});

      test('debería retornar la misma instancia sin argumentos', () {{
        // ARRANGE: crear instancia original
        // ACT: llamar copyWith() sin argumentos
        // ASSERT: expect(result, equals(original))
      }});
    }});

    group('props', () {{
      test('debería contener todos los campos en el orden correcto', () {{
        // ARRANGE: crear instancia
        // ACT: acceder a .props
        // ASSERT: expect(props, [{fields_str}])
      }});
    }});
  }});
}}
"""
    )
    return raw


def template_usecase(info: dict) -> str:
    cn = info['class_name']
    deps = info['dependencies']
    dep_type = deps[0]['type'] if deps else 'Repository'
    dep_name = deps[0]['name'] if deps else 'repository'
    dep_mock = mock_name(dep_type)
    dep_var = var_name(dep_name)

    methods = info['methods']
    call_method = next(
        (m for m in methods if m['name'] == 'call'), methods[0] if methods else None
    )
    method_name = call_method['name'] if call_method else 'call'

    raw = (
        format_imports(build_test_imports(info, 'domain_usecase'))
        + NL
        + f'class {dep_mock} extends Mock implements {dep_type} {{}}'
        + NL
        + NL
        + f"""void main() {{
  late {cn} useCase;
  late {dep_mock} {dep_var};

  setUp(() {{
    {dep_var} = {dep_mock}();
    useCase = {cn}({dep_name}: {dep_var});
  }});

  group('{cn}', () {{
    test(
      'debería retornar datos cuando la llamada es exitosa',
      () async {{
        // ARRANGE: configurar {dep_var}.{method_name}() para retornar un valor exitoso (Right)
        // ACT: ejecutar useCase(...)
        // ASSERT: verificar que retorna Right(...) con los datos esperados
        // ASSERT: verify(() => {dep_var}.{method_name}(...)).called(1)
      }},
    );

    test(
      'debería retornar Failure cuando la llamada falla',
      () async {{
        // ARRANGE: configurar {dep_var}.{method_name}() para retornar Left(ServerFailure(...))
        // ACT: ejecutar useCase(...)
        // ASSERT: verificar que retorna Left(ServerFailure)
        // ASSERT: verify(() => {dep_var}.{method_name}(...)).called(1)
      }},
    );

    test(
      'debería llamar al repositorio exactamente una vez',
      () async {{
        // ARRANGE: configurar {dep_var}.{method_name}() para retornar un valor exitoso
        // ACT: ejecutar useCase(...)
        // ASSERT: verify(() => {dep_var}.{method_name}(...)).called(1)
        // ASSERT: verifyNoMoreInteractions({dep_var})
      }},
    );
  }});
}}
"""
    )
    return raw


def template_model(info: dict) -> str:
    cn = info['class_name']
    imports = build_test_imports(info, 'data_model')
    fixture_import = get_helpers_import(info)
    fixture_name = info['file_name'].replace('_model', '')
    raw = (
        format_imports(imports)
        + fixture_import
        + NL
        + f"""void main() {{
  group('{cn}', () {{
    group('fromJson', () {{
      test('debería retornar un modelo válido desde JSON', () {{
        // ARRANGE: cargar fixture con fixtureAsMap('{fixture_name}')
        // ACT: llamar {cn}.fromJson(jsonMap)
        // ASSERT: verificar cada campo del modelo resultante
      }});

      test('debería lanzar error cuando falta un campo requerido', () {{
        // ARRANGE: crear JSON parcial sin campos required
        // ACT & ASSERT: expect(() => {cn}.fromJson(incomplete), throwsA(isA<TypeError>()))
      }});

      test('debería ignorar campos extra en el JSON', () {{
        // ARRANGE: crear JSON con campos adicionales
        // ACT: llamar {cn}.fromJson(jsonMap)
        // ASSERT: verificar que se crea el modelo correctamente
      }});
    }});

    group('toJson', () {{
      test('debería retornar un mapa JSON válido', () {{
        // ARRANGE: crear instancia del modelo
        // ACT: llamar model.toJson()
        // ASSERT: verificar keys y valores (incluyendo snake_case si aplica)
      }});
    }});

    group('roundtrip', () {{
      test('toJson + fromJson debería ser inverso', () {{
        // ARRANGE: crear instancia del modelo
        // ACT: json = model.toJson(); recreated = Model.fromJson(json)
        // ASSERT: expect(recreated, equals(original))
      }});
    }});

    group('entity conversion', () {{
      test('toEntity debería retornar Entity correcta', () {{
        // ARRANGE: crear instancia del modelo
        // ACT: llamar model.toEntity()
        // ASSERT: verificar que retorna isA<Entity>() con campos mapeados
      }});

      test('fromEntity debería crear Model desde Entity', () {{
        // ARRANGE: crear instancia de Entity
        // ACT: llamar Model.fromEntity(entity)
        // ASSERT: verificar que retorna isA<Model>() con campos copiados
      }});
    }});
  }});
}}
"""
    )
    return raw


def template_datasource(info: dict) -> str:
    cn = info['class_name']
    deps = info['dependencies']
    dep_type = deps[0]['type'] if deps else 'SupabaseClient'
    dep_name = deps[0]['name'] if deps else 'supabase'
    dep_mock = mock_name(dep_type)
    dep_var = var_name(dep_name)

    methods = info['methods']
    first_method = methods[0] if methods else None

    has_supabase = any(
        'supabase' in imp.lower() or 'gotrue' in imp.lower()
        for imp in info['imports']
    )

    fallback_lines = ''
    if has_supabase:
        fallback_lines = NL + """  setUpAll(() {
    registerFallbackValue(UserAttributes());
    registerFallbackValue(OtpType.signup);
    registerFallbackValue(OtpType.recovery);
  });"""

    method_block = ''
    if first_method:
        ret_type_clean = re.sub(r'Future<([^>]+)>', r'\1', first_method['return_type'])
        mname = first_method['name']
        raw_params = first_method['params_str']
        method_block = f"""
    test(
      'debería retornar {ret_type_clean} cuando {mname} es exitoso',
      () async {{
        // ARRANGE: configurar {dep_var}.{mname}(...) para retornar respuesta exitosa
        // ACT: llamar dataSource.{mname}({raw_params})
        // ASSERT: verificar que retorna el tipo esperado con datos correctos
      }},
    );

    test(
      'debería lanzar ServerException cuando falla {mname}',
      () async {{
        // ARRANGE: configurar {dep_var}.{mname}(...) para lanzar Exception
        // ACT & ASSERT: expect(() async => dataSource.{mname}(...), throwsA(isA<ServerException>()))
      }},
    );"""

    raw = (
        format_imports(build_test_imports(info, 'data_datasource'))
        + NL
        + f'class {dep_mock} extends Mock implements {dep_type} {{}}'
        + NL
        + fallback_lines
        + NL
        + NL
        + f"""void main() {{
  late {cn} dataSource;
  late {dep_mock} {dep_var};{fallback_lines}

  setUp(() {{
    {dep_var} = {dep_mock}();
    dataSource = {cn}({dep_name}: {dep_var});
  }});

  group('{cn}', () {{{method_block}
  }});
}}
"""
    )
    return raw


def template_repository(info: dict) -> str:
    cn = info['class_name']
    deps = info['dependencies']
    methods = info['methods']
    first_method = methods[0] if methods else None
    mname = first_method['name'] if first_method else 'method'

    dep0 = deps[0] if len(deps) > 0 else {'name': 'remoteDataSource', 'type': 'RemoteDataSource'}
    dep1 = deps[1] if len(deps) > 1 else None
    dep2 = deps[2] if len(deps) > 2 else None

    m0 = mock_name(dep0['type'])
    v0 = var_name(dep0['name'])
    m1 = mock_name(dep1['type']) if dep1 else ''
    v1 = var_name(dep1['name']) if dep1 else ''
    m2 = mock_name(dep2['type']) if dep2 else ''
    v2 = var_name(dep2['name']) if dep2 else ''

    mock_decls = f'  late {m0} {v0};'
    if dep1:
        mock_decls += f'{NL}  late {m1} {v1};'
    if dep2:
        mock_decls += f'{NL}  late {m2} {v2};'

    mock_inits = f'    {v0} = {m0}();'
    if dep1:
        mock_inits += f'{NL}    {v1} = {m1}();'
    if dep2:
        mock_inits += f'{NL}    {v2} = {m2}();'

    ctor_args = f'      {dep0["name"]}: {v0},'
    if dep1:
        ctor_args += f'{NL}      {dep1["name"]}: {v1},'
    if dep2:
        ctor_args += f'{NL}      {dep2["name"]}: {v2},'

    raw = (
        format_imports(build_test_imports(info, 'data_repository'))
        + NL
        + f'class {m0} extends Mock implements {dep0["type"]} {{}}'
        + (f'{NL}class {m1} extends Mock implements {dep1["type"]} {{}}' if dep1 else '')
        + (f'{NL}class {m2} extends Mock implements {dep2["type"]} {{}}' if dep2 else '')
        + NL
        + NL
        + f"""void main() {{
  late {cn} repository;
{mock_decls}

  setUpAll(() {{
    registerFallbackValue(const UserModel(id: 'fallback', email: 'fallback@test.com'));
  }});

  setUp(() {{
{mock_inits}
    repository = {cn}(
{ctor_args}
    );
  }});

  group('{cn}', () {{
    group('{mname} (online)', () {{
      test('debería retornar datos cuando la llamada remota es exitosa', () async {{
        // ARRANGE: mockNetworkInfo.isConnected retorna true
        // ARRANGE: mockRemoteDataSource.{mname}() retorna modelo exitoso
        // ACT: ejecutar repository.{mname}(...)
        // ASSERT: expect(result, isA<Right<Failure, ...>>())
      }},
      );

      test('debería retornar ServerFailure cuando falla la llamada remota', () async {{
        // ARRANGE: mockNetworkInfo.isConnected retorna true
        // ARRANGE: mockRemoteDataSource.{mname}() lanza ServerException
        // ACT: ejecutar repository.{mname}(...)
        // ASSERT: result.fold((l) => expect(l, isA<ServerFailure>()), (r) => fail('Expected Left'))
      }},
      );
    }});

    group('{mname} (offline)', () {{
      test('debería retornar NetworkFailure cuando está offline', () async {{
        // ARRANGE: mockNetworkInfo.isConnected retorna false
        // ACT: ejecutar repository.{mname}(...)
        // ASSERT: result.fold((l) => expect(l, isA<NetworkFailure>()), (r) => fail('Expected Left'))
      }},
      );

      test('no debería llamar al remoteDataSource cuando está offline', () async {{
        // ARRANGE: mockNetworkInfo.isConnected retorna false
        // ACT: ejecutar repository.{mname}(...)
        // ASSERT: verifyZeroInteractions(mockRemoteDataSource)
      }},
      );
    }});
  }});
}}
"""
    )
    return raw


def template_state(info: dict) -> str:
    cn = info['class_name']
    content = info.get('content', '')
    state_classes = re.findall(r'class\s+(\w+)\s+extends\s+\w+State', content)

    test_blocks = []
    for sc in state_classes:
        if sc == cn:
            continue
        test_blocks.append(f"""
    group('{sc}', () {{
      test('debería crear {sc} correctamente', () {{
        // ARRANGE & ACT: crear instancia
        // ASSERT: verificar que se crea sin errores
      }});

      test('debería tener props en el orden correcto', () {{
        // ARRANGE: crear instancia
        // ACT: acceder a .props
        // ASSERT: expect(state.props, [...])
      }});

      test('debería ser igual con los mismos valores', () {{
        // ARRANGE: crear dos instancias iguales
        // ASSERT: expect(state1, equals(state2))
      }});
    }});""")

    all_blocks = ''.join(test_blocks)
    raw = (
        format_imports(build_test_imports(info, 'presentation_state'))
        + NL
        + f"""void main() {{
  group('{cn}', () {{{all_blocks}
  }});
}}
"""
    )
    return raw


def template_cubit(info: dict) -> str:
    cn = info['class_name']
    deps = info['dependencies']
    content = info.get('content', '')

    state_name = None
    for m in re.finditer(r'class\s+\w+\s+extends\s+Cubit<(\w+)>', content):
        state_name = m.group(1)

    mock_decls = ''
    mock_inits = ''
    ctor_args = ''

    if deps:
        mock_decls = NL.join(f'  late {mock_name(d["type"])} {var_name(d["name"])};' for d in deps)
        mock_inits = NL.join(f'    {var_name(d["name"])} = {mock_name(d["type"])}();' for d in deps)
        ctor_lines = [f'      {d["name"]}: {var_name(d["name"])},' for d in deps]
        ctor_args = NL + NL.join(ctor_lines)

    raw = (
        format_imports(build_test_imports(info, 'presentation_cubit'))
        + NL
        + NL.join(f'class {mock_name(d["type"])} extends Mock implements {d["type"]} {{}}'
                  for d in deps if d['type'] != 'dynamic')
        + (NL if deps else '')
        + NL
        + f"""void main() {{
  late {cn} cubit;
{mock_decls}

  setUp(() {{
{mock_inits}
    cubit = {cn}({ctor_args}
    );
  }});

  tearDown(() {{
    cubit.close();
  }});

  group('{cn}', () {{
    test('debería tener estado inicial correcto', () {{
      // ASSERT: expect(cubit.state, isA<{state_name or 'InitialState'}>())
    }});

    test('debería emitir estados correctos en flujo exitoso', () {{
      // usar blocTest:
      // blocTest(
      //   'descripción',
      //   build: () => cubit,
      //   act: (cubit) => cubit.metodo(...),
      //   expect: () => [LoadingState, SuccessState],
      //   verify: (_) {{ verify(() => mockDep.llamada(...)).called(1); }},
      // );
    }});

    test('debería emitir estados de error cuando falla', () {{
      // ARRANGE: configurar mock.UseCase(any()) para retornar Left(ServerFailure(...))
      // ACT & ASSERT: blocTest con expect: () => [LoadingState, ErrorState]
    }});
  }});
}}
"""
    )
    return raw


def template_widget(info: dict) -> str:
    cn = info['class_name']
    content = info.get('content', '')
    cubit_type = None
    for m in re.finditer(r'(?:final|late)\s+(\w+Cubit\b)', content):
        cubit_type = m.group(1)

    state_type = 'dynamic'
    if cubit_type:
        for m in re.finditer(rf'class\s+{cubit_type}\s+extends\s+Cubit<(\w+)>', info.get('content', '')):
            state_type = m.group(1)

    if not cubit_type:
        raw = (
            format_imports(build_test_imports(info, 'presentation_widget'))
            + NL
            + f"""void main() {{
  group('{cn}', () {{
    testWidgets('debería renderizar correctamente', (WidgetTester tester) async {{
      // ACT: await tester.pumpWidget(MaterialApp(home: {cn}()))
      // ASSERT: expect(find.byType({cn}), findsOneWidget)
    }});
  }});
}}
"""
        )
        return raw

    mc = mock_name(cubit_type)
    mc_var = var_name(f'mock{cubit_type}')

    raw = (
        format_imports(build_test_imports(info, 'presentation_widget'))
        + NL
        + f'class {mc} extends Mock implements {cubit_type} {{}}'
        + NL
        + NL
        + f"""void main() {{
  late {mc} {mc_var};

  setUp(() {{
    {mc_var} = {mc}();
    when(() => {mc_var}.state).thenReturn({state_type}());
    when(() => {mc_var}.stream).thenAnswer((_) => const Stream.empty());
    when(() => {mc_var}.close()).thenAnswer((_) async {{}});
  }});

  Widget createWidgetUnderTest() {{
    return BlocProvider<{cubit_type}>.value(
      value: {mc_var},
      child: const MaterialApp(
        home: {cn}(),
      ),
    );
  }}

  group('{cn}', () {{
    testWidgets('debería renderizar correctamente', (WidgetTester tester) async {{
      // ACT: await tester.pumpWidget(createWidgetUnderTest())
      // ASSERT: expect(find.byType({cn}), findsOneWidget)
    }});

    testWidgets('debería mostrar estado de carga', (WidgetTester tester) async {{
      // ARRANGE: when(() => mock{cubit_type}.state).thenReturn(LoadingState())
      // ACT: await tester.pumpWidget(createWidgetUnderTest())
      // ASSERT: expect(find.byType(CircularProgressIndicator), findsOneWidget)
    }});

    testWidgets('debería manejar interacciones de usuario', (WidgetTester tester) async {{
      // ARRANGE: await tester.pumpWidget(createWidgetUnderTest())
      // ACT: await tester.tap(find.text('Botón')); await tester.pump()
      // ASSERT: verify(() => mock{cubit_type}.metodo()).called(1)
    }});
  }});
}}
"""
    )
    return raw


def template_core_service(info: dict) -> str:
    cn = info['class_name']
    deps = info['dependencies']

    mock_decls = ''
    mock_inits = ''
    ctor_args = ''
    if deps:
        mock_decls = NL.join(f'  late {mock_name(d["type"])} {var_name(d["name"])};' for d in deps)
        mock_inits = NL.join(f'    {var_name(d["name"])} = {mock_name(d["type"])}();' for d in deps)
        ctor_lines = [f'      {d["name"]}: {var_name(d["name"])},' for d in deps]
        ctor_args = NL + NL.join(ctor_lines)

    raw = (
        format_imports(build_test_imports(info, 'core_service'))
        + NL
        + NL.join(f'class {mock_name(d["type"])} extends Mock implements {d["type"]} {{}}'
                  for d in deps if d['type'] != 'dynamic')
        + (NL if deps else '')
        + NL
        + f"""void main() {{
  late {cn} service;
{mock_decls}

  setUp(() {{
{mock_inits}
    service = {cn}({ctor_args}
    );
  }});

  group('{cn}', () {{
    test('debería ejecutar la operación correctamente', () async {{
      // ARRANGE: configurar mocks
      // ACT: llamar service.metodo(...)
      // ASSERT: verificar resultado y llamados a mocks
    }});

    test('debería manejar errores correctamente', () async {{
      // ARRANGE: configurar mocks para lanzar excepción
      // ACT & ASSERT: verificar que el error se maneja sin propagarse
    }});
  }});
}}
"""
    )
    return raw


def template_core_generic(info: dict) -> str:
    cn = info['class_name']
    deps = info['dependencies']

    if not deps:
        raw = (
            format_imports(build_test_imports(info, 'core_generic'))
            + NL
            + f"""void main() {{
  group('{cn}', () {{
    test('debería ejecutarse correctamente', () {{
      // ARRANGE: preparar datos de entrada
      // ACT: ejecutar la función/método
      // ASSERT: verificar resultado esperado
    }});

    test('debería manejar edge cases', () {{
      // ARRANGE: preparar datos límite (null, vacío, etc.)
      // ACT: ejecutar con datos límite
      // ASSERT: verificar comportamiento esperado
    }});
  }});
}}
"""
        )
        return raw

    mock_decls = NL.join(f'  late {mock_name(d["type"])} {var_name(d["name"])};' for d in deps)
    mock_inits = NL.join(f'    {var_name(d["name"])} = {mock_name(d["type"])}();' for d in deps)
    ctor_lines = [f'      {d["name"]}: {var_name(d["name"])},' for d in deps]
    ctor_args = NL + NL.join(ctor_lines)

    raw = (
        format_imports(build_test_imports(info, 'core_generic'))
        + NL
        + NL.join(f'class {mock_name(d["type"])} extends Mock implements {d["type"]} {{}}'
                  for d in deps if d['type'] != 'dynamic')
        + (NL if deps else '')
        + NL
        + f"""void main() {{
  late {cn} service;
{mock_decls}

  setUp(() {{
{mock_inits}
    service = {cn}({ctor_args}
    );
  }});

  group('{cn}', () {{
    test('debería ejecutar la operación correctamente', () async {{
      // ARRANGE: configurar mocks
      // ACT: ejecutar servicio
      // ASSERT: verificar resultado y llamados a mocks
    }});
  }});
}}
"""
    )
    return raw


TEMPLATES = {
    'domain_entity': template_entity,
    'domain_usecase': template_usecase,
    'data_model': template_model,
    'data_datasource': template_datasource,
    'data_repository': template_repository,
    'presentation_state': template_state,
    'presentation_cubit': template_cubit,
    'presentation_page': template_widget,
    'presentation_widget': template_widget,
    'core_network': template_core_service,
    'core_service': template_core_service,
    'core_error': template_core_generic,
    'core_generic': template_core_generic,
}

LAYER_NAMES = {
    'domain_entity': 'Domain Entity',
    'domain_usecase': 'Domain UseCase',
    'data_model': 'Data Model',
    'data_datasource': 'Data DataSource',
    'data_repository': 'Data Repository',
    'presentation_state': 'Presentation State',
    'presentation_cubit': 'Presentation Cubit',
    'presentation_page': 'Presentation Page',
    'presentation_widget': 'Presentation Widget',
    'core_network': 'Core Network',
    'core_service': 'Core Service',
    'core_error': 'Core Error',
    'core_generic': 'Core Generic',
}


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 generate_test.py <path/to/file.dart>")
        print("")
        print("Genera un archivo de test boilerplate para un archivo Dart")
        print("siguiendo los patrones de Clean Architecture + Mocktail + bloc_test.")
        print("")
        print("Ejemplos:")
        print("  python3 generate_test.py apps/mobile/lib/features/auth/domain/usecases/sign_in.dart")
        print("  python3 generate_test.py lib/features/profile/data/models/user_profile_model.dart")
        sys.exit(1)

    source_path = sys.argv[1]

    if not os.path.exists(source_path):
        print(f"Error: Archivo no encontrado: {source_path}")
        sys.exit(1)

    if not source_path.endswith('.dart'):
        print(f"Error: No es un archivo Dart: {source_path}")
        sys.exit(1)

    if '/lib/' not in source_path.replace('\\', '/'):
        print(f"Error: El archivo debe estar dentro de lib/: {source_path}")
        sys.exit(1)

    pubspec_dir = find_pubspec_dir(source_path)
    if not pubspec_dir:
        print("Error: No se encontró pubspec.yaml en la jerarquía del archivo")
        sys.exit(1)

    try:
        info = parse_dart_file(source_path, pubspec_dir)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    layer = detect_layer(source_path)
    info['layer'] = layer

    if layer not in TEMPLATES:
        print(f"Error: No hay template para la capa detectada: {layer}")
        print(f"Path: {source_path}")
        sys.exit(1)

    generator = TEMPLATES[layer]
    test_content = generator(info)

    test_path = get_test_path(source_path)
    test_path = os.path.normpath(test_path)

    write_file(test_path, test_content + NL)

    layer_name = LAYER_NAMES.get(layer, layer)
    print(f"Test generado: {test_path}")
    print(f"  Capa: {layer_name}")
    print(f"  Clase: {info['class_name']}")
    if info['dependencies']:
        dep_list = ', '.join(d['type'] for d in info['dependencies'])
        print(f"  Dependencias: {dep_list}")
    print("")
    print("Edita el archivo de test y completa los cuerpos de los tests")
    print("siguiendo los comentarios en lenguaje natural.")


if __name__ == '__main__':
    main()
