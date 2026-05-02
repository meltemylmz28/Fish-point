import 'package:flutter/material.dart';
import 'package:frontend/providers/theme_provider.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:provider/provider.dart'; // MultiProvider ve ChangeNotifierProvider için
import 'providers/cart_provider.dart';     // CartProvider'ı tanıyabilmesi için

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => CartProvider()), // 4.3 aktif edildi[cite: 1]
        ChangeNotifierProvider(create: (_) => ThemeProvider()),
      ],
      child: const FishPointApp(),
    ),
  );
}

class FishPointApp extends StatelessWidget {
  const FishPointApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Fish-point',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const AdviceScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class AdviceScreen extends StatefulWidget {
  const AdviceScreen({super.key});

  @override
  State<AdviceScreen> createState() => _AdviceScreenState();
}

class _AdviceScreenState extends State<AdviceScreen> {
  String advice = "Tavsiye yükleniyor...";
  bool isLoading = true;
  String? errorMessage;
  String spotName = "Zamantı Irmağı Eğner";

  @override
  void initState() {
    super.initState();
    fetchAdvice();
  }

  Future<void> fetchAdvice() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      // Windows için localhost, Android emülatör için 10.0.2.2
      final response = await http.get(
        Uri.parse('http://127.0.0.1:8000/api/advice/1/'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          advice = data['advice'];
          spotName = data['spot_name'];
          isLoading = false;
        });
      } else {
        setState(() {
          errorMessage = 'Hata: ${response.statusCode}';
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Bağlantı hatası: $e\n\nDjango sunucusu çalışıyor mu?\nhttp://127.0.0.1:8000/api/advice/1/';
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🐟 Fish-point | Balıkçılık Danışmanı'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: fetchAdvice,
            tooltip: 'Yenile',
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: fetchAdvice,
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Center(
            child: isLoading
                ? const Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      CircularProgressIndicator(),
                      SizedBox(height: 16),
                      Text('Tavsiye alınıyor...'),
                    ],
                  )
                : errorMessage != null
                    ? Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.error_outline, size: 64, color: Colors.red),
                          const SizedBox(height: 16),
                          Text(
                            errorMessage!,
                            textAlign: TextAlign.center,
                            style: const TextStyle(color: Colors.red),
                          ),
                          const SizedBox(height: 24),
                          ElevatedButton.icon(
                            onPressed: fetchAdvice,
                            icon: const Icon(Icons.refresh),
                            label: const Text('Tekrar Dene'),
                          ),
                        ],
                      )
                    : SingleChildScrollView(
                        child: Card(
                          elevation: 4,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                          child: Padding(
                            padding: const EdgeInsets.all(20.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    const Icon(Icons.location_on, color: Colors.blue),
                                    const SizedBox(width: 8),
                                    Text(
                                      spotName,
                                      style: const TextStyle(
                                        fontSize: 18,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ],
                                ),
                                const Divider(height: 24),
                                Text(
                                  advice,
                                  style: const TextStyle(
                                    fontSize: 16,
                                    height: 1.6,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ),
          ),
        ),
      ),
    );
  }
}