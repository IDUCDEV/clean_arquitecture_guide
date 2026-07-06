import 'package:flutter_test/flutter_test.dart';
import 'package:mvp_template/app.dart';

void main() {
  testWidgets('App should render without errors', (WidgetTester tester) async {
    await tester.pumpWidget(const App());
    expect(find.text('Reservar Cancha'), findsOneWidget);
  });
}
