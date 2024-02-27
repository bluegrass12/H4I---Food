import 'package:flutter/material.dart';
import 'package:flutter/services.dart';


const produceList = ['Leafy Greens', 'Melons', 'Peppers'];

class InputHome extends StatelessWidget {
  const InputHome({super.key});

  static const routeName = '/input';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Add Data'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
             Padding(
              padding: const EdgeInsets.all(8.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Text("Produce Type:",style: Theme.of(context).textTheme.headlineSmall,),
                  const ProduceMenu(),
                  ],
              ),
            ),
            const Padding(
              padding:  EdgeInsets.all(16.0),
              child:  ProduceForm(),
            ),
          ],
        ),
      ),
    );
  }
}


class ProduceMenu extends StatefulWidget {
  const ProduceMenu({super.key});

  @override
  State<ProduceMenu> createState() => _ProduceMenuState();
}

class _ProduceMenuState extends State<ProduceMenu> {
  String dropdownValue = produceList.first;
  @override
  Widget build(BuildContext context) {
    return DropdownMenu(
      initialSelection: dropdownValue,
      dropdownMenuEntries: produceList.map<DropdownMenuEntry<String>>((String value) => DropdownMenuEntry(value: value, label: value)).toList(),
      onSelected: (String? value) {
        setState(() {
          dropdownValue = value!;
        });
      },

      
      );
  }
}


class ProduceForm extends StatefulWidget {
  const ProduceForm({super.key});

  @override
  State<ProduceForm> createState() => _ProduceFormState();
}

class _ProduceFormState extends State<ProduceForm> {
  final _formkey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formkey,
      child: Column(
        children: [
          TextFormField(
                  decoration: const InputDecoration(
                    labelText: 'Harvest Location',
                    hintText: 'Enter address of harvest location',
                  ),

                  validator: (value) {
                    if (value == null || value.isEmpty){
                      return 'Please enter the weight of the produce';
                    }
                    return null;
                  },
                ),
          Row(
            children: [
              Expanded(
                child: TextFormField(
                  decoration: const InputDecoration(
                    labelText: 'Quantity',
                    hintText: 'Produce Quantity',
                  ),
                  keyboardType: TextInputType.number,
                  // Only allows digits and decimal numbers
                  inputFormatters: <TextInputFormatter>[
                    FilteringTextInputFormatter.allow(RegExp(r'^\d*\.?\d*'))
                  ],
                  validator: (value) {
                    if (value == null || value.isEmpty || int.parse(value) <= 0){
                      return 'Please enter the quantity of produce';
                    }
                    return null;
                  },
                ),
              ),
              const SizedBox(width: 30,),
              Expanded(
                flex: 2,
                child: TextFormField(
                  decoration: const InputDecoration(
                    labelText: 'Unit of measure',
                    hintText: 'Unit type',
                  ),

                  validator: (value) {
                    if (value == null || value.isEmpty){
                      return 'Please enter the unit of measure';
                    }
                    return null;
                  },
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: () {
              if (_formkey.currentState!.validate()) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Processing Data')),
                );
              }
            },
            child: const Text('Submit'),
          ),
        ],
      )
      );
  }
}