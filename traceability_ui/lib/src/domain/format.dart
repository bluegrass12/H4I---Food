
import 'package:equatable/equatable.dart';

class Format extends Equatable{
  final String name;
  final int startRow;
  final int startColumn;
  final String eventType;
  final Map<String,int> kdeFormat;

  const Format({
    required this.name,
    required this.startRow,
    required this.startColumn,
    required this.eventType,
    required this.kdeFormat,
  });

  Map<String, dynamic> toMap() {
    return{
       name:{       
      'start_row': startRow,
      'start_column': startColumn,
      'event_type': eventType,
      'format': kdeFormat,}
    };
  }

  factory Format.fromMap(Map<String, dynamic> map, String name) {
    return Format(
      name: name,
      startRow: map['start_row'],
      startColumn: map['start_column'],
      eventType: map['event_type'],
      kdeFormat: Map<String,int>.from(map['format']),
    );
  }

  @override
  String toString() {
    return "Name: $name, Start Row: $startRow, Start Column: $startColumn, Event Type: $eventType, Format: $kdeFormat";
  }
  
  @override
  // TODO: implement props
  List<Object?> get props => [name];
}