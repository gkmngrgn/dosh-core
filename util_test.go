package dosh

import "testing"

var (
	languageCodes = []struct {
		value, want string
	}{
		{"en_US.UTF-8", "en"},
		{"de_DE.UTF-8", "en"}, // fallback language, we don't support de for now.
		{"tr_TR.UTF-8", "tr"},
		{"", "en"},
	}
	helpTextLines = []struct {
		value, want string
	}{
		{"command 1", "command 1           "},
		{"bla-bla-bla-bla-bla", "bla-bla-bla-bla-bla "},
		{"foo", "foo                 "},
		{"what if I write a too long command?", "what if I write a too long command?"},
	}
)

func TestGetLanguage(t *testing.T) {
	for _, lang := range languageCodes {
		if langCode := GetLanguage(lang.value); langCode != lang.want {
			t.Fatalf("Actual: %s, Expected: %s", langCode, lang.want)
		}
	}
	t.Log(len(languageCodes), "test cases")
}

func TestPadLength(t *testing.T) {
	for _, text := range helpTextLines {
		if alignedText := LeftPad(text.value, 20); alignedText != text.want {
			t.Fatalf("Actual: %s, Expected: %s", alignedText, text.want)
		}
	}
}
