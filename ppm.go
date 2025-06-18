/*
// Copyright 2025 Omega Labs
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
*/

package main

import (
	"fmt"
	"os"
	"os/user"
	"ppm/ppmcore"

	"github.com/fatih/color"
)

const Version string = "0.1"

var helpText = `Usage: ppm [options] <command>

ppm is a command-line package manager currently under testing.
If you encounter any issues while using ppm, please report them at: https://github.com/the-OmegaLabs/ppm/issues

This software is licensed under the Apache License v2.0.

Common commands:
init         Initialize configuration files and software sources
`

var (
	warnColor = color.New(color.FgYellow)
	failColor = color.New(color.FgRed)
	infoColor = color.New(color.FgBlue)
	doneColor = color.New(color.FgGreen)
)

func isPipe() bool {
	fi, err := os.Stdin.Stat()
	if err != nil {
		return false
	}

	return fi.Mode()&os.ModeNamedPipe != 0
}

func colorLn(c *color.Color, text string) {
	c.Print("<>")
	fmt.Println(" " + text)
}

func checkRoot() bool {
	var err bool = false

	usr, _ := user.Current()

	if usr.Uid != "0" { // check root
		colorLn(failColor, "This operation requires administrative privileges.")
		err = true
	}

	return err
}

func checkEnv() bool {
	var failed bool = false

	if isPipe() {
		colorLn(failColor, "This program cannot be run from a pipe.")
		failed = true
	}

	if err := os.MkdirAll("/var/ppm/", 0755); err != nil {
		colorLn(failColor, fmt.Sprintf("Failed to create /var/ppm/: %v", err))
		failed = true
	}

	if err := os.MkdirAll("/etc/ppm/", 0755); err != nil {
		colorLn(failColor, fmt.Sprintf("Failed to create /var/ppm/: %v", err))
		failed = true
	}

	return failed
}

func main() {
	// fmt.Println("ppm", Version)

	if checkEnv() { // check environment
		return
	}

	if len(os.Args) < 2 {
		fmt.Println(helpText)
		return
	}

	cmd := os.Args[1]

	switch cmd {
	case "version":
		colorLn(infoColor, "Plusto Package Manager")
		colorLn(infoColor, "ppm-cli version "+Version)
		colorLn(infoColor, "ppm-core version "+ppmcore.Version)

		fmt.Println()

		colorLn(infoColor, "Copyright 2025 (Stevesuk0 <stevesukawa@outlook.com>)")
		colorLn(infoColor, "Licensed under the Apache License, Version 2.0")
		colorLn(infoColor, "You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0")

	case "hello":
		fmt.Println(ppmcore.Hello())
	}

}
