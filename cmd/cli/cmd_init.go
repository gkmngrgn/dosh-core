package main

import (
	"fmt"
	"os"
	"strings"
)

var yamlTemplate = `
environments:
    - DEV
    - PROD
    - TEST
aliases:
    docker: docker-compose -f docker-compose.yml -f docker-compose.${ENV}.yml
commands:
    start:
        help_text: Create and start containers
        run: ${docker} up -d ${ARGS}
    build:
        help_text: Build or rebuild services
        run: ${docker} build ${ARGS}
    shell:
        run: ${docker} run --rm backend-shell bash
    initdb:
        environments:
            - DEV
        help_text: Load fixtures for development environment
        run: ${docker} run --rm backend-shell python manage.py initdb
`

func initConf(conf string) {
	if _, err := os.Stat(conf); err == nil {
		fmt.Printf(getText("err-conf-exists"), conf)
		return
	}

	file, err := os.Create(conf)
	if err != nil {
		panic(err)
	}

	file.WriteString(strings.TrimSpace(yamlTemplate))
	file.Sync()

	fmt.Printf(getText("msg-init-conf"), conf)
}
