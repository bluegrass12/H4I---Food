# food_tracing

## Goals

The goal of this project is to create a simple application to help producers input their data into a digital system, store it, and be able to export it to members further up the supply chain

## About Flutter

Flutter is a cross-development framework based on the Dart language. Developed by Google, there is plenty of documentation out there to help someone quickly pick it up. In general, you can think of the widgets (parts of the app) being arranged in a tree-like structure where every widget is the child of another widget (except the root widget).

For help getting started with Flutter development, view the
[online documentation](https://flutter.dev/docs), which offers tutorials,
samples, guidance on mobile development, and a full API reference.

## Current State

Currently this app is only a skeleton. A basic input form exists, but no data is stored and no backend exists. For state-management, this application currently uses the Flutter riverpod package (specifically its generator package). The settings/theme information doesn't use that state-management because it is an artifact from a template I used for this project, but may be changed in the future.

## Localization

This project generates localized messages based on arb files found in
the `lib/src/localization` directory.

To support additional languages, please visit the tutorial on
[Internationalizing Flutter
apps](https://flutter.dev/docs/development/accessibility-and-localization/internationalization)
