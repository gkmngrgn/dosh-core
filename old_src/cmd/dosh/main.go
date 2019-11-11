package main

import (
	"flag"
	"fmt"
	"os"

	"dosh"
)

var (
	flagConf *string
)

func init() {
	flagConf = flag.String("c", dosh.DefaultConf, "config file")
}

func printVersion() {
	fmt.Printf("%s %s\n", dosh.AppName, dosh.AppVersion)
}

func main() {
	if len(os.Args) == 1 {
		printVersion()
	}

	flag.Parse()
	dosh.RunCommand(*flagConf, os.Args[1:])
}
