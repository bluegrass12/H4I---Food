
import 'package:flutter/material.dart';
import 'package:food_tracing/src/features/data_input/input_home.dart';
import 'package:food_tracing/src/features/history/history_page.dart';
import 'package:food_tracing/src/features/home/main_home.dart';
import 'package:food_tracing/src/features/routing/core_shell.dart';
import 'package:food_tracing/src/settings/settings_controller.dart';
import 'package:food_tracing/src/settings/settings_view.dart';
import 'package:go_router/go_router.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';


part 'router.g.dart';


// Router Provider
// Initial Example from this site: https://github.com/flutter/flutter/issues/112915
// Another Example found here (closer to this implementation): https://github.com/lucavenir/go_router_riverpod/blob/master/firebase_example/lib/router.dart
 
// By using a global key, Flutter doesn't have to rebuild the full router everytime it updates
final navigatorKey = GlobalKey<NavigatorState>();

// The router needs access to ref (so it can see the auth state)
// Thus, it needs to be in itos own provider

@riverpod
GoRouter router(RouterRef ref, SettingsController settingsController) {

  return GoRouter(
    initialLocation: InputHome.routeName,
    navigatorKey: navigatorKey,
    routes:[
      // A Shell Route keeps the bottom app bar and scaffold (The shell) and only updates the body
      ShellRoute(
        pageBuilder:  (BuildContext context, GoRouterState state, Widget child ) => NoTransitionPage(child: AppShell(child: child)),
        routes: <RouteBase>[
          GoRoute(path: MainHome.routeName, pageBuilder: (context, state) => const NoTransitionPage(child: MainHome())),
          GoRoute(
            path: InputHome.routeName,
            pageBuilder: (context, state) => const NoTransitionPage(child: InputHome()),
            ),
          GoRoute(
            path: HistoryHome.routeName,
            pageBuilder: (context, state) => const NoTransitionPage(child:HistoryHome()),
            ),
            
          // Clubs
          GoRoute(
            path: SettingsView.routeName,
            pageBuilder: (context, state) => NoTransitionPage(child: SettingsView(controller: settingsController)),
          )
        ]
        )
    ],

  );
}