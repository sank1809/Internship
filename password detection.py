import secrets
import string
import time
import hashlib
import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List
import sqlite3


class Score(Enum):
    VERY_WEAK = 1
    WEAK = 2
    FAIR = 3
    GOOD = 4
    STRONG = 5


@dataclass
class AnalysisResult:
    strength: str
    score: Score
    estimated_crack_time: str
    checks: Dict[str, bool]
    suggestions: List[str]


class PasswordEvaluator:
    def __init__(self):
        self.init_db()

    def init_db(self):
        """Initialize SQLite database for password history (demo)"""
        try:
            self.conn = sqlite3.connect("passwords.db")
            self.conn.execute("""
                              CREATE TABLE IF NOT EXISTS passwords
                              (
                                  id
                                  INTEGER
                                  PRIMARY
                                  KEY
                                  AUTOINCREMENT,
                                  password_hash
                                  TEXT
                                  NOT
                                  NULL,
                                  timestamp
                                  DATETIME
                                  DEFAULT
                                  CURRENT_TIMESTAMP,
                                  score
                                  INTEGER
                              )
                              """)
            self.conn.commit()
        except Exception:
            self.conn = None

    def analyze(self, password: str) -> AnalysisResult:
        """Analyze password strength"""
        if not password:
            return AnalysisResult("Empty", Score.VERY_WEAK, "Instant", {}, ["Password cannot be empty"])

        checks = {
            "length": len(password) >= 12,
            "uppercase": any(c.isupper() for c in password),
            "lowercase": any(c.islower() for c in password),
            "digits": any(c.isdigit() for c in password),
            "special_chars": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password),
            "no_repetitive": not self._has_repetitive_chars(password),
            "no_common_words": not self._contains_common_words(password),
            "no_keyboard_patterns": not self._has_keyboard_pattern(password)
        }

        passed_count = sum(checks.values())
        score = Score(max(1, min(5, passed_count)))

        strength_map = {
            Score.VERY_WEAK: "Very Weak",
            Score.WEAK: "Weak",
            Score.FAIR: "Fair",
            Score.GOOD: "Good",
            Score.STRONG: "Strong"
        }

        crack_time_map = {
            Score.VERY_WEAK: "Instant",
            Score.WEAK: "Minutes",
            Score.FAIR: "Hours",
            Score.GOOD: "Days",
            Score.STRONG: "Centuries"
        }

        suggestions = self._generate_suggestions(checks, password)

        # Log to database (demo)
        if self.conn:
            try:
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                self.conn.execute(
                    "INSERT INTO passwords (password_hash, score) VALUES (?, ?)",
                    (password_hash, score.value)
                )
                self.conn.commit()
            except:
                pass

        return AnalysisResult(
            strength=strength_map[score],
            score=score,
            estimated_crack_time=crack_time_map[score],
            checks=checks,
            suggestions=suggestions
        )

    def _has_repetitive_chars(self, password: str) -> bool:
        """Check for repetitive characters"""
        for i in range(len(password) - 2):
            if password[i] == password[i + 1] == password[i + 2]:
                return True
        return False

    def _contains_common_words(self, password: str) -> bool:
        """Check for common words"""
        common_words = {
            "password", "123456", "qwerty", "admin", "letmein",
            "welcome", "monkey", "dragon", "master", "hello"
        }
        password_lower = password.lower()
        return any(word in password_lower for word in common_words)

    def _has_keyboard_pattern(self, password: str) -> bool:
        """Check for keyboard patterns like 'qwerty'"""
        patterns = ["qwerty", "asdf", "zxcv", "1234"]
        password_lower = password.lower()
        return any(pattern in password_lower for pattern in patterns)

    def _generate_suggestions(self, checks: Dict[str, bool], password: str) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []

        if not checks["length"]:
            suggestions.append("Use at least 12 characters")
        if not checks["uppercase"]:
            suggestions.append("Add uppercase letters")
        if not checks["lowercase"]:
            suggestions.append("Add lowercase letters")
        if not checks["digits"]:
            suggestions.append("Add numbers")
        if not checks["special_chars"]:
            suggestions.append("Add special characters (!@#$%)")
        if not checks["no_repetitive"]:
            suggestions.append("Avoid repetitive characters")
        if not checks["no_common_words"]:
            suggestions.append("Avoid common words like 'password'")
        if not checks["no_keyboard_patterns"]:
            suggestions.append("Avoid keyboard patterns like 'qwerty'")

        if not suggestions:
            suggestions.append("Great password! Consider making it longer for extra security.")

        return suggestions

    def generate_strong_password(self, length: int = 16) -> str:
        """Generate a strong random password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(chars) for _ in range(length))
        return password


def main():
    """Interactive CLI interface"""
    evaluator = PasswordEvaluator()

    print("🔐 Password Strength Evaluator")
    print("=" * 50)

    while True:
        print("\n1. Evaluate password")
        print("2. Generate strong password")
        print("3. Clear password history (demo)")
        print("4. Exit")

        choice = input("\nChoose option: ").strip()

        if choice == "1":
            password = input("Enter password to evaluate: ").strip()
            if password:
                analysis = evaluator.analyze(password)
                print("\n📊 Analysis Results:")
                print(f"Strength: {analysis.strength} ({analysis.score.value}/8)")
                print(f"Crack time: {analysis.estimated_crack_time}")
                print("\n✅ Checks passed:")
                for check, passed in analysis.checks.items():
                    status = "✅" if passed else "❌"
                    print(f"  {status} {check.replace('_', ' ').title()}")
                print("\n💡 Suggestions:")
                for suggestion in analysis.suggestions:
                    print(f" • {suggestion}")

        elif choice == "2":
            print("💡 Enter a NUMBER for length (8-50) or press Enter for default (16)")
            length_input = input("Password length: ").strip()

            if not length_input:  # Empty input = default
                length = 16
            else:
                try:
                    length = int(length_input)
                    if length < 8:
                        print("⚠️  Minimum length is 8. Using 16 instead.")
                        length = 16
                    elif length > 50:
                        print("⚠️  Maximum length is 50. Using 32 instead.")
                        length = 32
                except ValueError:
                    print("❌ Invalid input! Using default length 16.")
                    length = 16

            strong_pw = evaluator.generate_strong_password(length)
            print(f"\n🔑 Generated password ({length} chars): {strong_pw}")
            analysis = evaluator.analyze(strong_pw)
            print(f"💪 Strength: {analysis.strength}")
            print(f"📈 Score: {analysis.score.value}/8")

        elif choice == "3":
            try:
                if evaluator.conn:
                    evaluator.conn.close()
                if os.path.exists("passwords.db"):
                    os.remove("passwords.db")
                    print("✅ Password history cleared!")
                else:
                    print("ℹ️  No password history file found")
            except Exception as e:
                print(f"❌ Error clearing history: {e}")

        elif choice == "4":
            if evaluator.conn:
                evaluator.conn.close()
            print("Goodbye! 👋")
            break

        else:
            print("❌ Invalid choice! Please select 1-4.")


if __name__ == "__main__":
    main()
