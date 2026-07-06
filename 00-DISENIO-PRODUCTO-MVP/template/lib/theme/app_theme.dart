import 'package:flutter/material.dart';
import 'app_colors.dart';
import 'app_extensions.dart';
import 'app_typography.dart';

class AppTheme {
  AppTheme._();

  static ThemeData light() => _base(AppColors.light());

  static ThemeData dark() => _base(AppColors.dark());

  static ThemeData _base(ColorScheme colorScheme) {
    return ThemeData(
      useMaterial3: true,
      colorScheme: colorScheme,
      textTheme: AppTypography.textTheme,
      visualDensity: VisualDensity.adaptivePlatformDensity,
    ).copyWith(
      extensions: const <ThemeExtension<dynamic>>[
        AppSpacing(),
        AppRadii(),
      ],
    );
  }
}
