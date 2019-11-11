package dosh

import (
	"errors"
	"fmt"

	"github.com/logrusorgru/aurora"
)

type verbosity int

const (
	VerbosityQUIET verbosity = iota - 1
	VerbosityNORMAL
	VerbosityDEBUG
)

const appVerbosity = VerbosityNORMAL // TODO: get the verbosity from the settings

func renderMessage(v verbosity, msg string, args ...interface{}) (string, error) {
	if appVerbosity == VerbosityQUIET && v > appVerbosity {
		return "", errors.New("insufficient verbosity")
	}
	return fmt.Sprintf(msg, args...), nil
}

type Logger interface {
	info(v verbosity, msg string, args ...interface{})
	success(v verbosity, msg string, args ...interface{})
	error(v verbosity, msg string, args ...interface{})
}

// Log func WHY SHOULD I WRITE COMMENT FOR ALL EXPORTED FUNCS?!
type Log struct{}

func (l Log) error(v verbosity, msg string, args ...interface{}) {
	if msg, err := renderMessage(v, msg, args...); err == nil {
		fmt.Println(aurora.Red(msg))
	}
}

func (l Log) success(v verbosity, msg string, args ...interface{}) {
	if msg, err := renderMessage(v, msg, args...); err == nil {
		fmt.Println(aurora.Green(msg))
	}
}

func (l Log) info(v verbosity, msg string, args ...interface{}) {
	if msg, err := renderMessage(v, msg, args...); err == nil {
		fmt.Println(aurora.White(msg))
	}
}
