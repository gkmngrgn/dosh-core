package dosh

import (
	"strings"
)

var (
	languages = []string{
		FallbackLanguage,
		"tr",
	}
)

// GetLanguage - parses LANG environment and returns the supported language code.
func GetLanguage(lang string) string {
	if len(lang) < 2 {
		return FallbackLanguage
	}

	// TODO: add Windows support.
	lang = strings.Split(lang, ".")[0][:2]
	for _, language := range languages {
		if language == lang {
			return lang
		}
	}
	return FallbackLanguage
}

// LeftPad - adds empty spaces to align help texts vertically.
func LeftPad(text string, length int) string {
	textLength := len(text)
	if length < textLength {
		length = textLength
	}
	return text + strings.Repeat(" ", length-textLength)
}
