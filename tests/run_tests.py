import subprocess
import sys
import os


def run_simple_tests():
    print("Запускаем тесты CRM системы")
    print("=" * 40)

    test_files = [
        "tests/test_services.py",
        "tests/test_business_rules.py",
        "tests/test_full_flow.py"
    ]

    passed = 0
    failed = 0

    for test_file in test_files:
        print(f"\nТестируем: {test_file}")
        print("-" * 30)

        try:
            result = subprocess.run(
                ["pytest", test_file, "-v"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("Успешно")
                passed += 1
            else:
                print("Ошибки:")
                for line in result.stderr.split('\n')[:5]:
                    if line.strip():
                        print(f"   {line}")
                failed += 1

        except Exception as e:
            print(f"Ошибка запуска: {e}")
            failed += 1

    print("\n" + "=" * 40)
    print(f"ИТОГИ:")
    print(f"Успешно: {passed}")
    print(f"Ошибки: {failed}")

    if failed == 0:
        print("\nВсе тесты прошли! Система готова.")
        return True
    else:
        print(f"\nЕсть ошибки в {failed} тестах")
        return False


if __name__ == "__main__":
    success = run_simple_tests()
    sys.exit(0 if success else 1)