#! /usr/bin/env python3
import subprocess

EXPECTED_MESSAGE = b'Your Message has been received: b\'"Test message sent by netcat."\''
SUCCESS_MESSAGE = "Test message received OK"
FAILURE_MESSAGE = "Test message not received correctely"

def build():
    build_command = 'docker build -f ./Dockerfile -t test:latest .'
    process = subprocess.Popen(build_command.split())
    process.communicate()


def run_and_check():
    run_command = "docker run --network=tp0-dockercomposeinit_testing_net test:latest"
    process = subprocess.Popen(run_command.split(), stdout = subprocess.PIPE)
    output, _err = process.communicate()

    assert(output.strip() == EXPECTED_MESSAGE)

if __name__ == "__main__":
    build()

    try:
        run_and_check()
        print(SUCCESS_MESSAGE)
    except:
        print(FAILURE_MESSAGE)
