import 'package:flutter/material.dart';

class AppColors {
  AppColors._();

  static const Color seed = Color(0xFF1B5E20);

  static ColorScheme light() => ColorScheme.fromSeed(
        seedColor: seed,
        brightness: Brightness.light,
      );

  static ColorScheme dark() => ColorScheme.fromSeed(
        seedColor: seed,
        brightness: Brightness.dark,
      );
}
