package main

import (
	"os"

	"dosh"
)

var (
	translations = map[string]map[string]string{
		"en": {
			"commands":            "COMMANDS",
			"cmd-gen-desc":        "generate shell script to use commands without dosh",
			"cmd-help-desc":       "print this output",
			"cmd-init-desc":       "initialize a new dosh configuration file",
			"cmd-run-desc":        "run a dosh cmd reading configuration file directly",
			"cmd-vers-desc":       "print version of the app",
			"err-conf-exists":     "The file %s already exists. Please try a different one.",
			"flag-conf-desc":      "name of configuration file",
			"flag-gen-force-desc": "overwrite if the file exists",
			"flag-gen-shell-desc": "determine shell type (bash, pwsh, etc.)",
			"msg-init-conf":       "Initial configuration is ready now: %s",
			"options":             "OPTIONS",
			"usage":               "Usage",
		},
		"tr": {
			"commands":            "KOMUTLAR",
			"cmd-gen-desc":        "dosh yüklemeden kullanmak için betik oluştur",
			"cmd-help-desc":       "bu çıktıyı yazdır",
			"cmd-init-desc":       "yeni bir dosh yapılandırma dosyası oluştur",
			"cmd-run-desc":        "dosh yapılandırma dosyasını okuyarak komut çalıştır",
			"cmd-vers-desc":       "uygulamanın sürümünü yazdır",
			"err-conf-exists":     "%s dosyası zaten var. Başka bir tane deneyin.",
			"flag-conf-desc":      "yapılandırma dosyasının ismi",
			"flag-gen-force-desc": "dosya varsa üzerine yaz",
			"flag-gen-shell-desc": "betik dilini belirt (bash, pwsh, vs.)",
			"msg-init-conf":       "Örnek yapılandırma doyanız hazır: %s",
			"options":             "SEÇENEKLER",
			"usage":               "Kullanım",
		},
	}
)

func getText(textKey string) string {
	lang := os.Getenv("LANG")
	return translations[dosh.GetLanguage(lang)][textKey]
}
