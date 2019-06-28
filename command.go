package dosh

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"sort"
	"strings"

	"gopkg.in/yaml.v2"
)

type DoshCommand struct {
	HelpText     string   `yaml:"help_text"`
	Run          string   `yaml:"run"`
	Environments []string `yaml:"environments"`
}

type DoshConfig struct {
	Environments []string               `yaml:"environments"`
	Aliases      map[string]string      `yaml:"aliases"`
	Commands     map[string]DoshCommand `yaml:"commands"`
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
		"Available Environments",
		strings.Join(textEnvironments, "\n"),
		"",
		"Available Commands",
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
