package ppmcore

import (
	"encoding/json"
	"os"
	"os/user"
)

type Repo struct {
	Name     string `json:"name"`
	Type     string `json:"type"`
	URL      string `json:"url"`
	Codename string `json:"codename"`
	Category string `json:"category"`
}

const Version string = "0.1"

func checkRoot() bool {
	usr, _ := user.Current()
	return usr.Uid == "0"
}

func EnableLock(lockPath string) bool {
	if !checkRoot() {
		return false
	}

	file, err := os.Create(lockPath + "/ppm.lock")
	if err != nil {
		return false
	}
	defer file.Close()
	return true
}

func DisableLock(lockPath string) bool {
	if !checkRoot() {
		return false
	}
	err := os.Remove(lockPath + "/ppm.lock")
	return err == nil
}

func CheckLock(lockPath string) bool {
	if !checkRoot() {
		return false
	}
	_, err := os.Stat(lockPath + "/ppm.lock")
	return err == nil
}

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
		return err
	}

	return nil
}
