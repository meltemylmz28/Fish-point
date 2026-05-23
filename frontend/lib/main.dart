import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'package:frontend/providers/auth_provider.dart';
import 'package:frontend/providers/spot_provider.dart';
import 'package:frontend/providers/cart_provider.dart';
import 'package:frontend/providers/theme_provider.dart';
import 'package:frontend/screens/advice_screen_fixed.dart';
import 'package:frontend/screens/login_screen.dart';

const Color powderPink = Color(0xFFFFD1DC);
const Color navyBlue = Color(0xFF000080);

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => SpotProvider()),
        ChangeNotifierProvider(create: (_) => CartProvider()),
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
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        scaffoldBackgroundColor: powderPink,
        appBarTheme: const AppBarTheme(backgroundColor: navyBlue, foregroundColor: powderPink),
        primaryColor: navyBlue,
        useMaterial3: true,
      ),
      home: const AuthWrapper(),
    );
  }
}

class AuthWrapper extends StatefulWidget {
  const AuthWrapper({super.key});

  @override
  State<AuthWrapper> createState() => _AuthWrapperState();
}

class _AuthWrapperState extends State<AuthWrapper> {
  bool _loading = true;
  bool _authenticated = false;

  @override
  void initState() {
    super.initState();
    _checkLogin();
  }

  Future<void> _checkLogin() async {
    final auth = context.read<AuthProvider>();
    final success = await auth.tryAutoLogin();
    if (!mounted) return;
    setState(() {
      _authenticated = success;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return _authenticated ? const AdviceScreen() : const LoginScreen();
  }
}
