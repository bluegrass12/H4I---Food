// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'router.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

String _$routerHash() => r'a2ae1e07ac4f5d92862fd54a02667ef0e4df63ad';

/// Copied from Dart SDK
class _SystemHash {
  _SystemHash._();

  static int combine(int hash, int value) {
    // ignore: parameter_assignments
    hash = 0x1fffffff & (hash + value);
    // ignore: parameter_assignments
    hash = 0x1fffffff & (hash + ((0x0007ffff & hash) << 10));
    return hash ^ (hash >> 6);
  }

  static int finish(int hash) {
    // ignore: parameter_assignments
    hash = 0x1fffffff & (hash + ((0x03ffffff & hash) << 3));
    // ignore: parameter_assignments
    hash = hash ^ (hash >> 11);
    return 0x1fffffff & (hash + ((0x00003fff & hash) << 15));
  }
}

/// See also [router].
@ProviderFor(router)
const routerProvider = RouterFamily();

/// See also [router].
class RouterFamily extends Family<GoRouter> {
  /// See also [router].
  const RouterFamily();

  /// See also [router].
  RouterProvider call(
    SettingsController settingsController,
  ) {
    return RouterProvider(
      settingsController,
    );
  }

  @override
  RouterProvider getProviderOverride(
    covariant RouterProvider provider,
  ) {
    return call(
      provider.settingsController,
    );
  }

  static const Iterable<ProviderOrFamily>? _dependencies = null;

  @override
  Iterable<ProviderOrFamily>? get dependencies => _dependencies;

  static const Iterable<ProviderOrFamily>? _allTransitiveDependencies = null;

  @override
  Iterable<ProviderOrFamily>? get allTransitiveDependencies =>
      _allTransitiveDependencies;

  @override
  String? get name => r'routerProvider';
}

/// See also [router].
class RouterProvider extends AutoDisposeProvider<GoRouter> {
  /// See also [router].
  RouterProvider(
    SettingsController settingsController,
  ) : this._internal(
          (ref) => router(
            ref as RouterRef,
            settingsController,
          ),
          from: routerProvider,
          name: r'routerProvider',
          debugGetCreateSourceHash:
              const bool.fromEnvironment('dart.vm.product')
                  ? null
                  : _$routerHash,
          dependencies: RouterFamily._dependencies,
          allTransitiveDependencies: RouterFamily._allTransitiveDependencies,
          settingsController: settingsController,
        );

  RouterProvider._internal(
    super._createNotifier, {
    required super.name,
    required super.dependencies,
    required super.allTransitiveDependencies,
    required super.debugGetCreateSourceHash,
    required super.from,
    required this.settingsController,
  }) : super.internal();

  final SettingsController settingsController;

  @override
  Override overrideWith(
    GoRouter Function(RouterRef provider) create,
  ) {
    return ProviderOverride(
      origin: this,
      override: RouterProvider._internal(
        (ref) => create(ref as RouterRef),
        from: from,
        name: null,
        dependencies: null,
        allTransitiveDependencies: null,
        debugGetCreateSourceHash: null,
        settingsController: settingsController,
      ),
    );
  }

  @override
  AutoDisposeProviderElement<GoRouter> createElement() {
    return _RouterProviderElement(this);
  }

  @override
  bool operator ==(Object other) {
    return other is RouterProvider &&
        other.settingsController == settingsController;
  }

  @override
  int get hashCode {
    var hash = _SystemHash.combine(0, runtimeType.hashCode);
    hash = _SystemHash.combine(hash, settingsController.hashCode);

    return _SystemHash.finish(hash);
  }
}

mixin RouterRef on AutoDisposeProviderRef<GoRouter> {
  /// The parameter `settingsController` of this provider.
  SettingsController get settingsController;
}

class _RouterProviderElement extends AutoDisposeProviderElement<GoRouter>
    with RouterRef {
  _RouterProviderElement(super.provider);

  @override
  SettingsController get settingsController =>
      (origin as RouterProvider).settingsController;
}
// ignore_for_file: type=lint
// ignore_for_file: subtype_of_sealed_class, invalid_use_of_internal_member, invalid_use_of_visible_for_testing_member
