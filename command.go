package dosh

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strings"

	"github.com/logrusorgru/aurora"
	"gopkg.in/yaml.v2"
)

const (
	actionMKDIR = "MKDIR"
	actionPRINT = "PRINT"
	actionRUN   = "RUN"
)

var doshConfig = Config{}

type (
	// StringArray can be just a string or a string array.
	StringArray []string

	// SubCommand structure includes a sub-command info that specified by the user.
	SubCommand struct {
		HelpText     string      `yaml:"help_text"`
		Run          StringArray `yaml:"run"`
		Environments []string    `yaml:"environments"`
	}

	// Config structure is for parsing the user configuration file.
	Config struct {
		Environments []string              `yaml:"environments"`
		Aliases      map[string]string     `yaml:"aliases"`
		Commands     map[string]SubCommand `yaml:"commands"`
	}
)

// UnmarshalYAML - A quick solution to allow some fields in multiple types.
// https://github.com/go-yaml/yaml/issues/100#issuecomment-324964723
func (a *StringArray) UnmarshalYAML(unmarshal func(interface{}) error) error {
	var multi []string
	err := unmarshal(&multi)
	if err != nil {
		var single string
		err := unmarshal(&single)
		if err != nil {
			return err
		}
		*a = []string{single}
	} else {
		*a = multi
	}
	return nil
}

// CheckConfigFile is an initial function to check the file existence and parsing as well.
func CheckConfigFile(conf string) error {
	data, err := ioutil.ReadFile(conf)
	if err != nil {
		return err
	}

	err = yaml.Unmarshal([]byte(string(data)), &doshConfig)
	if err != nil {
		return err
	}

	return nil
}

func getUsage(conf string) string {
	var textEnvironments, textCommands []string

	// Section: Environments
	for _, env := range doshConfig.Environments {
		textEnvironments = append(textEnvironments, fmt.Sprintf("  - %s", env))
	}
	sort.Strings(textEnvironments)

	// Section: Commands
	for name, cmd := range doshConfig.Commands {
		textCommands = append(textCommands,
			fmt.Sprintf("  > %s %s", LeftPad(name, 20), cmd.HelpText))
	}
	sort.Strings(textCommands)

	// Merge sections and return output with a default style
	helpOutput := []string{
		fmt.Sprint(aurora.Cyan("Available Environments")),
		strings.Join(textEnvironments, "\n"),
		"",
		fmt.Sprint(aurora.Cyan("Available Commands")),
		strings.Join(textCommands, "\n"),
	}
	return strings.Join(helpOutput, "\n")
}

// RunCommand func allows you to run commands from the yaml configuration without generating any
// shell script.
func RunCommand(conf string, args []string) {
	var l Logger = Log{} // we will use log module later.

	if err := CheckConfigFile(conf); err != nil {
		fmt.Println(aurora.Red(err.Error()))
		return
	}

	if len(args) == 0 {
		fmt.Println(getUsage(conf))
		os.Exit(0)
	}

	var success bool

	for index, subCmd := range doshConfig.Commands[args[0]].Run {
		parsed := strings.SplitN(subCmd, " ", 2)
		action := parsed[0]
		params := parsed[1]

		switch action {
		case actionMKDIR:
			l.info(VerbosityDEBUG, "%d. MKDIR", index+1)
			success = RunActionMkdir(l, params)
			break
		case actionPRINT:
			l.info(VerbosityDEBUG, "%d. PRINT", index+1)
			success = RunActionPrint(l, params)
			break
		case actionRUN:
			l.info(VerbosityDEBUG, "%d. RUN", index+1)
			success = RunActionRun(l, params)
			break
		default:
			l.error(VerbosityNORMAL, "Unknown action: %s", subCmd)
			success = false
			break
		}

		// do not continue if you get an error. all steps should be done successfully.
		if success == false {
			l.error(VerbosityDEBUG, "the last command was not success. it's stopped.")
			os.Exit(1)
		}
	}

	os.Exit(0)
}

func RunActionMkdir(l Logger, params string) bool {
	stat, err := os.Stat(params)
	if err != nil {
		err = os.Mkdir(params, 0700)
		return true
	}

	if !stat.IsDir() {
		l.error(VerbosityNORMAL, "There's a file with the same name.")
		return false
	}

	return true
}

func RunActionPrint(l Logger, params string) bool {
	fmt.Println(params)
	return true
}

func RunActionRun(l Logger, params string) bool {
	return true
}
