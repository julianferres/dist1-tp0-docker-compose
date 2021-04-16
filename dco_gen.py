# Script that initializes the docker compose with N parameters
import argparse, yaml


def generate_server():
    return {'server':
            {'container_name': 'server',
             'image': 'server:latest',
             'entrypoint': 'python3 /main.py',
             'environment':
                ['PYTHONUNBUFFERED=1',
                'SERVER_IP=server',
                'SERVER_PORT=12345',
                'SERVER_LISTEN_BACKLOG=5'],
             'networks': ['testing_net']
            }}


def generate_client(client_id):
    return {f'client{client_id}':
                {'container_name': f'client{client_id}',
                'image': 'client:latest',
                'entrypoint': '/client',
                'environment':[
                    f'CLI_ID={client_id}',
                    'CLI_SERVER_ADDRESS=server:12345',
                    'CLI_LOOP_LAPSE=1m2s',
                    'CLI_LOOP_PERIOD=10s'
                ],
                'networks': ['testing_net'],
                'depends_on': ['server']}
            }


def generate_description(n_clients):
    version = {'version': '3'}
    services = {'services': {}}
    network = { 'networks':
                {'testing_net':
                    {'ipam':
                        {'driver': 'default',
                         'config': [{'subnet': '172.25.125.0/24'}]}
                    }}}


    for k, v in generate_server().items():
        services['services'][k] = v

    for client_id in range(1, n_clients + 1):
        client_act = generate_client(client_id)

        for k, v in client_act.items():
            services['services'][k] = v
        
    return {**version, **services, **network}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('n_clients', type=int, help='number of clients to be created')

    args = parser.parse_args()
    
    print(f"Generating docker-compose description with {args.n_clients} clients...")

    with open('docker-compose-dev.yaml', 'w') as file:
        dict_file = generate_description(args.n_clients)
        yaml.dump(dict_file, file)


