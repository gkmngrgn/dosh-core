package main

import "testing"

func TestTranslations(t *testing.T) {
	// all keys should be translated in each language.
	translationCount := 13
	for _, langTranslations := range translations {
		if count := len(langTranslations); count != translationCount {
			t.Fatalf("Actual: %d, Expected: %d", count, translationCount)
		}
	}
}
