package ppmcore

import (
	"encoding/json"
	"fmt"
	"os"
)

type Repo struct {
	Name     string `json:"name"`
	Type     string `json:"type"`
	URL      string `json:"url"`
	Codename string `json:"codename"`
	Category string `json:"category"`
}

const Version string = "0.1"

func Hello() string {
	return "Hello, World!"
}

func InitConfig(configDir string) error {
	exampleRepo := []Repo{
		{
			Name:     "System Base",
			Type:     "dpkg",
			URL:      "http://mirrors.sdu.edu.cn/debian",
			Codename: "bookworm",
			Category: "main/binary-amd64",
		},
	}

	filePath := configDir + "/repo.json"
	f, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer f.Close()

	encoder := json.NewEncoder(f)
	encoder.SetIndent("", "    ")
	if err := encoder.Encode(exampleRepo); err != nil {
		return fmt.Errorf("failed to write json: %w", err)
	}

	return nil
}
