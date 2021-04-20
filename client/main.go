package main

import (
	"log"
	"time"

	"github.com/pkg/errors"
	"github.com/spf13/viper"

	"github.com/7574-sistemas-distribuidos/docker-compose-init/client/common"
)

// InitConfig Function that uses viper library to parse env variables. If
// some of the variables cannot be parsed, an error is returned
func InitConfig() (*viper.Viper, error) {
	v := viper.New()

	// Configure viper to read env variables with the CLI_ prefix
	v.AutomaticEnv()
	v.SetEnvPrefix("cli")

	//Add config file support
	v.BindEnv("config", "path")
	v.BindEnv("config", "name")

	if !v.IsSet("config_path") || !v.IsSet("config_name") {
		// Use env variables if not config file (as before this excersice)
		v.BindEnv("id")
		v.BindEnv("server", "address")
		v.BindEnv("loop", "period")
		v.BindEnv("loop", "lapse")
	} else {
		v.AddConfigPath(v.GetString("config_path"))
		v.SetConfigName(v.GetString("config_name"))

		if err := v.ReadInConfig(); err != nil {
			return nil, errors.Wrapf(err, "Could not parse config file.")
		}
	}

	// Parse time.Duration variables and return an error
	// if those variables cannot be parsed
	if _, err := time.ParseDuration(v.GetString("loop_lapse")); err != nil {
		return nil, errors.Wrapf(err, "Could not parse CLI_LOOP_LAPSE env var as time.Duration.")
	}

	if _, err := time.ParseDuration(v.GetString("loop_period")); err != nil {
		return nil, errors.Wrapf(err, "Could not parse CLI_LOOP_PERIOD env var as time.Duration.")
	}

	return v, nil
}

func main() {
	v, err := InitConfig()
	if err != nil {
		log.Fatalf("%s", err)
	}

	clientConfig := common.ClientConfig{
		ServerAddress: v.GetString("server_address"),
		ID:            v.GetString("id"),
		LoopLapse:     v.GetDuration("loop_lapse"),
		LoopPeriod:    v.GetDuration("loop_period"),
	}

	client := common.NewClient(clientConfig)
	client.StartClientLoop()
}
