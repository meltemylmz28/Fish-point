import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:provider/provider.dart';

// Provider importları[cite: 1]
import 'providers/auth_provider.dart';
import 'providers/spot_provider.dart';
import 'providers/cart_provider.dart';
import 'providers/theme_provider.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),   // 4.1 Aktif[cite: 1]
        ChangeNotifierProvider(create: (_) => SpotProvider()),   // 4.2 Aktif[cite: 1]
        ChangeNotifierProvider(create: (_) => CartProvider()),   // 4.3 Aktif[cite: 1]
        ChangeNotifierProvider(create: (_) => ThemeProvider()),   // 4.4 Aktif[cite: 1]
      ],
      child: const FishPointApp(),
    ),
  );
}

class FishPointApp extends StatelessWidget {
  const FishPointApp({super.key});

  @override
  Widget build(BuildContext context) {
    // Tema değişikliğini anlık dinlemek için provider'ı bağladık[cite: 1]
    final themeProvider = Provider.of<ThemeProvider>(context);

    return MaterialApp(
      title: 'Fish-point',
      debugShowCheckedModeBanner: false,
      // Tema modu provider'dan gelen veriye göre değişir
      themeMode: themeProvider.isDarkMode ? ThemeMode.dark : ThemeMode.light,
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: Colors.blue,
        brightness: Brightness.light,
      ),
      darkTheme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: Colors.blue,
        brightness: Brightness.dark,
      ),
      home: const AdviceScreen(),
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
      // Önemli Not: Android Emülatör kullanıyorsan 127.0.0.1 yerine 10.0.2.2 yazmalısın[cite: 1]
      final response = await http.get(
        Uri.parse('http://127.0.0.1:8000/api/advice/1/'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          advice = data['advice'] ?? "Tavsiye bulunamadı.";
          spotName = data['spot_name'] ?? "Bilinmeyen Bölge";
          isLoading = false;
        });
      } else {
        setState(() {
          errorMessage = 'Sunucu Hatası: ${response.statusCode}';
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Bağlantı hatası: $e\n\nLütfen Django sunucusunun çalıştığından emin ol.';
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('🐟 Fish-point'),
        centerTitle: true,
        actions: [
          // Tema değiştirme butonu testi için[cite: 1]
          IconButton(
            icon: Icon(context.watch<ThemeProvider>().isDarkMode
              ? Icons.light_mode
              : Icons.dark_mode),
            onPressed: () => context.read<ThemeProvider>().toggleTheme(),
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: fetchAdvice,
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: fetchAdvice,
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Center(
            child: isLoading
                ? const CircularProgressIndicator()
                : errorMessage != null
                    ? SingleChildScrollView(
                        physics: const AlwaysScrollableScrollPhysics(),
                        child: Column(
                          children: [
                            const Icon(Icons.cloud_off, size: 64, color: Colors.grey),
                            const SizedBox(height: 16),
                            Text(errorMessage!, textAlign: TextAlign.center),
                            ElevatedButton(
                              onPressed: fetchAdvice,
                              child: const Text('Tekrar Dene'),
                            ),
                          ],
                        ),
                      )
                    : SingleChildScrollView(
                        physics: const AlwaysScrollableScrollPhysics(),
                        child: Card(
                          elevation: 4,
                          child: Padding(
                            padding: const EdgeInsets.all(20.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    const Icon(Icons.location_on, color: Colors.blue),
                                    const SizedBox(width: 8),
                                    Expanded(
                                      child: Text(
                                        spotName,
                                        style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                                      ),
                                    ),
                                  ],
                                ),
                                const Divider(height: 24),
                                Text(advice, style: const TextStyle(fontSize: 16, height: 1.5)),
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