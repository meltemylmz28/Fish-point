import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'package:frontend/providers/auth_provider.dart';
import 'package:frontend/providers/spot_provider.dart';
import 'package:frontend/providers/cart_provider.dart';
import 'package:frontend/providers/theme_provider.dart';
import 'package:frontend/providers/favorites_provider.dart';
import 'package:frontend/screens/forgot_password_screen.dart';
import 'package:frontend/screens/welcome_screen.dart';
import 'package:frontend/screens/reset_password_screen.dart';
import 'package:frontend/screens/verify_email_screen.dart';
import 'package:frontend/screens/home/main_screen.dart';
import 'package:frontend/config.dart';
import 'package:frontend/theme/app_theme.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await AppConfig.init();
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ThemeProvider()..load()),
        ChangeNotifierProvider(create: (_) => AuthProvider()),
        ChangeNotifierProvider(create: (_) => SpotProvider()),
        ChangeNotifierProvider(create: (_) => CartProvider()),
        ChangeNotifierProvider(create: (_) => FavoritesProvider()),
      ],
      child: const FishPointApp(),
    ),
  );
}

class FishPointApp extends StatelessWidget {
  const FishPointApp({super.key});

  @override
  Widget build(BuildContext context) {
    final themeProvider = context.watch<ThemeProvider>();

    return MaterialApp(
      title: 'Fish-Point',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light(),
      darkTheme: AppTheme.dark(),
      themeMode: themeProvider.themeMode,
      home: const AuthWrapper(),
      routes: {
        '/login': (_) => const WelcomeScreen(),
        '/forgot-password': (_) => const ForgotPasswordScreen(),
        '/home': (_) => const MainScreen(),
      },
      onGenerateRoute: (settings) {
        final uri = Uri.parse(settings.name ?? '');

        if (uri.path == '/verify-email') {
          return MaterialPageRoute(
            builder: (_) => VerifyEmailScreen(
              uid: uri.queryParameters['uid'],
              token: uri.queryParameters['token'],
            ),
          );
        }

        if (uri.path == '/reset-password') {
          return MaterialPageRoute(
            builder: (_) => ResetPasswordScreen(
              uid: uri.queryParameters['uid'],
              token: uri.queryParameters['token'],
            ),
          );
        }

        return null;
      },
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
    final favorites = context.read<FavoritesProvider>();
    final success = await auth.tryAutoLogin();
    await favorites.load();
    if (!mounted) return;
    setState(() {
      _authenticated = success;
      _loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final fp = context.fp;

    if (_loading) {
      return Scaffold(
        backgroundColor: fp.scaffold,
        body: const Center(child: CircularProgressIndicator(color: AppColors.cyan)),
      );
    }

    return _authenticated ? const MainScreen() : const WelcomeScreen();
  }
}
