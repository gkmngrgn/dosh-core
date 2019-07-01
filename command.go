package dosh

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"sort"
	"strings"

	"github.com/logrusorgru/aurora"
	"gopkg.in/yaml.v2"
)

type StringArray []string

type DoshCommand struct {
	HelpText     string      `yaml:"help_text"`
	Run          StringArray `yaml:"run"`
	Environments []string    `yaml:"environments"`
}

type DoshConfig struct {
	Environments []string               `yaml:"environments"`
	Aliases      map[string]string      `yaml:"aliases"`
	Commands     map[string]DoshCommand `yaml:"commands"`
}

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

func getUsage(conf string) string {
	data, err := ioutil.ReadFile(conf)
	if err != nil {
		log.Fatal(err)
		return "" // TODO: better output
	}

	doshConfig := DoshConfig{}
	err = yaml.Unmarshal([]byte(string(data)), &doshConfig)
	if err != nil {
		log.Fatal(err)
		return "" // TODO: better output please
	}

	var textEnvironments, textCommands []string
	for _, env := range doshConfig.Environments {
		textEnvironments = append(textEnvironments, fmt.Sprintf("  - %s", env))
	}
	sort.Strings(textEnvironments)

	for name, cmd := range doshConfig.Commands {
		textCommands = append(textCommands,
			fmt.Sprintf("  > %s %s", LeftPad(name, 20), cmd.HelpText))
	}
	sort.Strings(textCommands)

	helpOutput := []string{
		fmt.Sprint(aurora.Cyan("Available Environments")),
		strings.Join(textEnvironments, "\n"),
		"",
		fmt.Sprint(aurora.Cyan("Available Commands")),
		strings.Join(textCommands, "\n"),
	}
	// return fmt.Sprintf("--- t:\n%v\n\n", doshConfig)
	return strings.Join(helpOutput, "\n")
}

// RunCommand func allows you to run commands from the yaml configuration without generating any
// shell script.
func RunCommand(conf string, args []string) {
	// TODO: check file here.
	if len(args) == 0 {
		fmt.Println(getUsage(conf))
		os.Exit(0)
	}

	fmt.Printf("Test for runCommand. Args: %s", strings.Join(args, ", "))
}
