import 'dart:convert';
import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:traceability_ui/src/settings/settings_view.dart';

import '../domain/format.dart';


class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('EPCIS - JSON Converter'),
        actions: <Widget>[
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
               context.goNamed(SettingsView.routeName);
            },
          ),
        ],
      ),
      body: const HomeBody(),
    );
  }

  
}

/// The body of the homescreen, handles selecting a file to convert and converting it
class HomeBody extends StatefulWidget {
  const HomeBody({super.key});

  @override
  State<HomeBody> createState() => _HomeBodyState();
}

class _HomeBodyState extends State<HomeBody> {

  final String _settingsPath = './SpreadsheetConverter/settings.json';

  List<Format>? _settings;
  Format? _currentFormat;
  FilePickerResult? _selectedFileResult;

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  @override
  Widget build(BuildContext context) {

    return (_selectedFileResult == null) ? 
    Center(
          child: Column( 
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text("Select a file to convert", style: Theme.of(context).textTheme.headlineMedium,),
              IconButton(
                iconSize: 150,
                icon: const Icon(Icons.upload_file),
                onPressed: () {
                  _selectFile(context);
                },
              ),
              const SizedBox(height: 20,),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text("Format:", style: Theme.of(context).textTheme.headlineSmall),
                  const SizedBox(width: 20,),
                  FormatDropdown(formatList: _settings, currentFormat: _currentFormat, onChanged: (format) => setState(() {
                    _currentFormat = format;
                  })),
                  IconButton(onPressed: (){}, iconSize:30, icon: const Icon(Icons.add)),
                ],
              ),
            ],
          ),
      )
      : Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextButton.icon(
              label: Text("Convert ${_selectedFileResult!.files.single.name}", style: Theme.of(context).textTheme.headlineMedium),
              icon: const Icon(Icons.upload_file, size: 50),
              onPressed: () {
                _convertFile(context);
              },
            ),
            const SizedBox(height: 20,),
            IconButton(
              iconSize: 50,
              icon: const Icon(Icons.cancel),
              onPressed: () {
                setState(() {
                  _selectedFileResult = null;
                });
              }
            )
          ],
        ),
      );
  }


  /// Selects a file to convert and updates the _selectedFileResult
  void _selectFile(BuildContext context) async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(type:FileType.custom, allowedExtensions: ['json','xlsx']);

    if (result != null) {
      setState(() {
        _selectedFileResult = result;
      });
      // Do something with the selected file
    } else {
      // User canceled the file selection
    }
  }


  /// Converts the _selectedFileResult using the python converter
  void _convertFile(BuildContext context) async {
    // Argument format: file to run, input file, output file, settings path, optional -f to specify format


    await Process.run('python', ['./SpreadsheetConverter/UI_converter_handler.py', _selectedFileResult!.files.single.path!, './SpreadsheetConverter/testUIOutput.json', _settingsPath]);
      // Listen to the error output from stderr
      // print(process.stdout);
      // print(process.stderr);
      setState(() {
        _selectedFileResult = null;
      });

  }

  /// Load settings from the settings file
  Future<void> _loadSettings() async {
    File settingsFile = File(_settingsPath);
    if (settingsFile.existsSync()) {
      String settingsString = await settingsFile.readAsString();
      Map<String, dynamic> settingsMap = jsonDecode(settingsString);
      setState(() {
          _settings = settingsMap['settings'].entries.map<Format>((entry) => Format.fromMap(entry.value, entry.key)).toList();
          _currentFormat = settingsMap['current_format'] != null ? Format.fromMap(settingsMap['settings'][settingsMap['current_format']], settingsMap['current_format']) : null;
      });

    }
    else{

    }
  }
}

class FormatDropdown extends StatelessWidget {
  const FormatDropdown({super.key, this.currentFormat, required this.formatList, required this.onChanged});

  final Format? currentFormat;
  final List<Format>? formatList;
  final ValueChanged<Format?>? onChanged;

  @override
  Widget build(BuildContext context) {
    if(formatList != null){
      return DropdownButton<Format>(
        value: currentFormat,
        items: formatList!.map<DropdownMenuItem<Format>>(
          (format) { 
            return DropdownMenuItem<Format>(
              value: format,
              child: Text(format.name),
            );
        }).toList(), 
        onChanged: onChanged);
    }
    else{
      return const Text("No formats found");
    }
    }

}