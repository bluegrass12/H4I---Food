
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:food_tracing/src/features/data_input/input_home.dart';
import 'package:food_tracing/src/features/history/history_page.dart';
import 'package:food_tracing/src/features/routing/router.dart';
import 'package:food_tracing/src/settings/settings_controller.dart';
import 'package:food_tracing/src/settings/settings_view.dart';
import 'package:go_router/go_router.dart';

import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

import '../home/main_home.dart';


class AppCore extends ConsumerWidget {
  const AppCore({super.key, required this.settingsController});
  final SettingsController settingsController;
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider(settingsController));

    return AnimatedBuilder(
      animation: settingsController,
      builder: (BuildContext context, Widget? child) {
        return MaterialApp.router(
          // Providing a restorationScopeId allows the Navigator built by the
          // MaterialApp to restore the navigation stack when a user leaves and
          // returns to the app after it has been killed while running in the
          // background.
          restorationScopeId: 'app',
          debugShowCheckedModeBanner: false,


          // Provide the generated AppLocalizations to the MaterialApp. This
          // allows descendant Widgets to display the correct translations
          // depending on the user's locale.
          localizationsDelegates: const [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
          ],
          supportedLocales: const [
            Locale('en', ''), // English, no country code
          ],

          // Use AppLocalizations to configure the correct application title
          // depending on the user's locale.
          //
          // The appTitle is defined in .arb files found in the localization
          // directory.
          onGenerateTitle: (BuildContext context) =>
              AppLocalizations.of(context)!.appTitle,

          // Define a light and dark color theme. Then, read the user's
          // preferred ThemeMode (light, dark, or system default) from the
          // SettingsController to display the correct theme.
          theme: ThemeData(),
          darkTheme: ThemeData.dark(),
          themeMode: settingsController.themeMode,
          // Define a function to handle named routes in order to support
          // Flutter web url navigation and deep linking.
          routerConfig: router,

          );
          },
        );
  }
}


// The scaffold and app bar that surrounds the main body of the app
// The AppShell contains everything that doesn't change between normal screen changes
class AppShell extends StatelessWidget {
  const AppShell({required this.child, super.key});
  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      body: child,
      bottomNavigationBar: const CustomNavBar(),
    );
  }
}

class CustomNavBar extends StatelessWidget {
  const CustomNavBar({super.key});

  @override
  Widget build(BuildContext context) {
    return NavigationBar(
      destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: "Home",),
          NavigationDestination(icon: Icon(Icons.add_outlined), selectedIcon: Icon(Icons.add), label: "Add Data",),
          NavigationDestination(icon: Icon(Icons.history_edu_outlined), selectedIcon: Icon(Icons.history_edu), label: "History"),
          NavigationDestination(icon: Icon(Icons.settings_outlined), selectedIcon: Icon(Icons.settings), label: "Settings"),
        ],
      selectedIndex: _getSelectedIndex(context),
      onDestinationSelected: (int index) => _handleSelection(index, context),
      labelBehavior: NavigationDestinationLabelBehavior.alwaysHide,
      );
  }

  // Converts the path of the currently selected page to the index of its icon 
  static int _getSelectedIndex(BuildContext context){
    final String location = GoRouterState.of(context).uri.path;
    if(location.startsWith(InputHome.routeName)) return 1;
    if(location.startsWith(HistoryHome.routeName)) return 2;
    if(location.startsWith(SettingsView.routeName)) return 3;
    // Defaults to selecting the home icon
    return 0;
  }

  // Navigates to the corresponding path when an appbar icon is tapped
  static void _handleSelection(int index, BuildContext context){
    switch(index){
      case 1:
        GoRouter.of(context).go(InputHome.routeName);
        break;
      case 2:
        GoRouter.of(context).go(HistoryHome.routeName);
        break;
      case 3: 
        GoRouter.of(context).go(SettingsView.routeName);
        break;
      default:
        GoRouter.of(context).go(MainHome.routeName);
        break;
    }
  }
}


  